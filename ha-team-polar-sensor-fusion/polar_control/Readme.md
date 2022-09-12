These packages rely on a few ros packages. To install do:
```
sudo apt-get install ros-noetic-effort-controllers ros-noetic-joy ros-noetic-ros-controllers ros-noetic-ros-control ros-noetic-gazebo-ros-control
```
catkin_make after installing.
To be able to control the polar_prototype the following launch files need to be run in seperate terminals
```
roslaunch polar_gazebo polar_emptyworld.launch
roslaunch polar_control polar_control.launch
```
You might get errors due to not having installed the correct packages. They will mostly say which package needs to be installed. Please add these packages to the above `apt-get install` command.

If you have a controller you can use the Left Stick to control the speed of the left wheels and Right stick to control the speed of the right wheels. Fully up is max speed forward and fully down is max speed backwards.

For running without a controller you can publish manually to the topic `/polar_prototype/cmd_vel`
You can also run it using your keyboard by doing `rosrun polar_control teleop_key_cmdvel.py`

There is some issues with the car not wanting to turn in place, but I can't figure out why (maybe too much grip?). Cornering should work fine. 

