## Instructions polar prototype urdf

First visualized using urdf tutorial: sudo apt install ros-noetic-urdf-tutorial

then run command: roslaunch urdf_tutorial display.launch model:=urdf/polar_prototype.urdf


frame bounding box: x=800 x y=1120 x z=500 mm

wheel position y = 519, x = 435

## Skid steering

For now the [skid-steering plugin](http://gazebosim.org/tutorials?tut=ros_gzplugins) from ros-gazebo is used to do skid steering. This plugin listens to the polar_prototype/cmd_vel topic, you can publish linear velocity in x-dir and angular around z. Publishing other velocities in the Twist message is possible but it will not do anything with it. 

Inertia tensors of the frame and wheels were obtained in Meshlab according to [this guide] (http://gazebosim.org/tutorials?tut=inertia). 

An attempt was also made at using effort controllers for the vehicle. This made steering less fluent and since we will probably be sending cmd_vel data to the Avular Prime anyways using the plugin made sense. 

At the moment steering is still very wobbly and weird. Although the vehicle does eventually steer it bumps around a lot. Main guess at the moment is that this is caused by the friction coefficients, the max torque, contact area of the wheels or misalignment in the wheels (that the axle isn't centered). For now it is enough that the vehicle steers but when the vehicle is built a second optimization can be done to ensure it behaves the same in simulation as in real life. 

A lot of the values in the URDF were also stolen from other URDF files such as the Pioneer 3AT  which uses skid steering [link to urdf](https://github.com/MobileRobots/amr-ros-config/blob/master/description/urdf/pioneer3at.urdf.xacro). 

