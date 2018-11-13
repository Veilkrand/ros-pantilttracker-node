# Pan-tilt Tracker

Get poses messages from a `marker-tracker-node` and send Twist messages to a `pantilt-node` to correct the error to the center of the camera.

## TODO: 
 - Tune the PID better.

## Pantilt_node params
```
topic = '/cmd_pantilt'
tilt = Twist.linear.x  # [-1,1]
pan = Twist.angular.z  # [-1,1]
```

## Running

`roslaunch pantilt_tracker_node default.launch`


## Dependencies

### simple-pid
https://pypi.org/project/simple-pid/