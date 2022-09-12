# How to use and properly start the driver

After you have cloned the repository for the radar driver aka umrr_driver you also need to add some permisions and some missing libraries in order to properly start the node.
All these additional steps will be documented in the follwoing chapters.

For more additional technical information regarding the configration of the radar driver, please use the README.md file present in this package.
Here you'll find the day to day process for starting the driver and making it work properly on your system.
# Eddit the permision for read/write for scripts
After you have cloned/unziped the driver package you'll need to add the following permission for the follwoing scripts.
* sudo chmod +x /scripts/pc2_filter.py
* sudo chmod +x /scripts/spherical_coord_2_cartesian_coord.py
* sudo chmod +x /scripts/umrr_can_publisher.py

If you don't chmod the scripts the node will fail to start.
# Adding missing library
Furthermore there is a library that need to be added because it does not come as standard with Ubuntu 20.04 LTS
* sudo apt-get install crc16

The library is a must becuase otherwise the node will fail to start.
# Adding useful app
In order to properly test and debug the can port you can use the can-utils tool:
* sudo apt-get install can-utils

You can find more information on its github [page](https://github.com/linux-can/can-utils).

    
# Enableing the can driver
First thing to in order to set up the driver you need to add the can driver port in the cfg file.
* you can find the file in cfg/umrr_driver_default_config.yaml

Here you need to add the port:

```
radar/umrr_can_publisher:
  // parameters to send to sensor
  // antenna_mode: {section: 2010, parameter: 0, value: 2}
  //center_frequency: {section: 3016, parameter: 5, value: 2, dim: 0}
  // necessary parameters
  can_spec: "$(find umrr_driver)/can_spec/Automotive_Can_Spec_TargetList_V5.json"
  can_socket: "can0"
  legacy_mode: False
  // omit empty strings to be set by node (must not be edited by user)
  sensor_type: ""
  software_vers: ""
  curr_antenna: ""
```


After you added the port aka the can_socket vriable set to the can port that you ar listening to
You can either dump the port in order to check if the data is comming in:
* candump can0

Furthermore everytime you restart pc/relaunch the visualization you'll need to reopen the can port as follows:
* sudo ip link set can0 type can bitrate 500000 restart-ms 100
* sudo ip link set can0 up



# Correct Initialization of the driver
1. Start the can driver and start listening to the can0 port
    * sudo ip link set can0 type can bitrate 500000 restart-ms 100
    * sudo ip link set can0 up
2. running either:
    * roslaunch umrr_driver automotive_radar_default.launch
    * roslaunch umrr_driver automotive_radar_visualization.launch
