#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from polar_control.msg import CustomMsg
import sys

class Converter:
    def __init__(self):
        self.pub_RL = rospy.Publisher('wheel_RL_controller/command', Float64, queue_size=2)
        self.pub_RR = rospy.Publisher('wheel_RR_controller/command', Float64, queue_size=2)
        self.pub_FL = rospy.Publisher('wheel_FL_controller/command', Float64, queue_size=2)
        self.pub_FR = rospy.Publisher('wheel_FR_controller/command', Float64, queue_size=2)
        
        rospy.Subscriber('cmd_drive', CustomMsg, self.callback)
        rospy.spin()

    def callback(self, data):
        self.pub_RL.publish(data.drive.left_vel)
        self.pub_FL.publish(data.drive.left_vel)
        self.pub_RR.publish(data.drive.right_vel)
        self.pub_FR.publish(data.drive.right_vel)
    
if __name__ == '__main__':
    rospy.init_node('cmd_drive_converter', anonymous=True)
    converter = Converter()
