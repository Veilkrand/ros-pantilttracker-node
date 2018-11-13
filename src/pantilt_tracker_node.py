#!/usr/bin/env python
from __future__ import print_function
import rospy

from markertracker_node.msg import Marker, MarkersArray
from geometry_msgs.msg import Twist
from pantilt_controller import PanTiltController


class Subscriber(object):

    def __init__(self, input_topic, output_topic, rate, controller):

        self.controller = controller

        self.rospy_rate = rate
        self.latest_msg = None
        self.new_msg_available = False
        self.subscriber = rospy.Subscriber(input_topic, MarkersArray, self._callback, queue_size=1)

        self._pantilt_publisher = rospy.Publisher(output_topic, Twist, queue_size=1)

        self._loop()

    def _callback(self, data):
        self.latest_msg = data
        self.new_msg_available = True

    def _process_msg(self, data):
        return self.controller.process_markers(data)

    def _create_twist_msg_from_output(self, output):

        _msg = Twist()
        _msg.angular.z = output[0]
        _msg.linear.x = output[1]

        return _msg


    def _loop(self):

        r = rospy.Rate(self.rospy_rate)

        while not rospy.is_shutdown():
            if self.new_msg_available:
                self.new_msg_available = False

                output = self._process_msg(self.latest_msg)

                # Publish output
                if output is not None:
                    _twist_msg = self._create_twist_msg_from_output(output)
                    self._pantilt_publisher.publish(_twist_msg)

                # rospy.loginfo(msg)
                r.sleep()


if __name__ == '__main__':

    _node_name = 'pantilt_tracker_node'

    print('* {} starting... '.format(_node_name), end="")

    rospy.init_node(_node_name, anonymous=True)

    # Params. TODO: setup in launch file
    _input_topic = rospy.get_param("~markers_topic", '/markertracker_node/markers')
    _output_topic = rospy.get_param("~pantilt_topic", '/cmd_pantilt')
    _marker_target_id = rospy.get_param("~marker_target_id", 10)
    _rospy_rate = rospy.get_param("~rate", 60)

    controller = PanTiltController(_marker_target_id)
    Subscriber(_input_topic, _output_topic, _rospy_rate, controller)
