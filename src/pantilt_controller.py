#!/usr/bin/env python
"""
from simple_pid import PID
pid = PID(1, 0.1, 0.05, setpoint=1)

# assume we have a system we want to control in controlled_system
v = controlled_system.update(0)

while True:
    # compute new ouput from the PID according to the systems current value
    control = pid(v)

    # feed the PID output to the system and get its current value
    v = controlled_system.update(control)
"""

from __future__ import print_function

import pantilthat as pt
from simple_pid import PID

import math

class PanTiltController(object):

    def __init__(self, marker_target_id=None):

        self.marker_target_id = marker_target_id


        ## PID SETUP

        '''
        # 0.01, , 0.001
        #_sample_time = 0.01
        _kp = 0.01 # 0.01
        _ki = 0.00001 #0.001 #0.01
        _kd = 0.001 #0.0015
        '''

        # _sample_time = 0.01
        _kp = 0.0007
        _ki = 0.0 #0.00001
        _kd = 0.0

        self.pid_pan = PID(_kp, _ki, _kd, setpoint=0)
        self.pid_pan.output_limits = (-1, 1)
        self.pid_pan.proportional_on_measurement = False
        #self.pid_pan.sample_time = _sample_time

        self.pid_tilt = PID(_kp, _ki, _kd, setpoint=0)
        self.pid_tilt.output_limits = (-1, 1)
        self.pid_tilt.proportional_on_measurement = False
        #self.pid_tilt.sample_time = _sample_time


    def process_markers(self, data):

        markers = data.marker

        if len(markers) == 0 or self.marker_target_id is None: return None

        for marker in markers:

            if marker.id == self.marker_target_id:

                x = marker.translation_vector.x
                y = marker.translation_vector.y
                z = marker.translation_vector.z

                print('Marker:' ,x, y, z)


                # Calculate PID ouputs with input
                pan_output = self.pid_pan(x)
                tilt_output = self.pid_tilt(y)

                print('Pantilt Output:', pan_output,tilt_output)

                return pan_output, tilt_output

        return None




    ### TODO: Implement message to pantilt_node with the PID output. Adjust to spected scale [-1,1]

    ## Test. It didn't work as expected
    def _translation_to_angles(self, translation_vector):

        x = translation_vector.x
        y = translation_vector.y
        z = translation_vector.z

        print(x, y, z)

        if abs(x) > 0.05:
            rad = math.atan2(x,z)
            pan = math.degrees(rad)
            pt.pan(int(pan)*-1)
            print('pan:', pan)
        if abs(y) > 0.05:
            rad = math.atan2(y,z)
            tilt = math.degrees(rad)
            pt.tilt(int(tilt))
            print('tilt', tilt)



    ## Test, to delete

    def _pan_until_value_is_zero(self, value):

        _step = 0.5
        _dead_zone = 10

        if value > 0 + _dead_zone:
            self.pan -= _step

        if value < 0 - _dead_zone:
            self.pan += _step

        pt.pan(int(self.pan))

    def _tilt_until_value_is_zero(self, value):

        _step = 0.5
        _dead_zone = 10

        if value > 0 + _dead_zone:
            self.tilt += _step

        if value < 0 - _dead_zone:
            self.tilt -= _step

        pt.tilt(int(self.tilt))


