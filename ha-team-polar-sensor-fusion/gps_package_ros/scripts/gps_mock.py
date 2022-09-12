#!/usr/bin/env python3

# Import required Python code.
import roslib

import rospy
from std_msgs.msg import String
# Create a callback function for the subscriber.
def callback(data):
    # Simply print out values in our custom message.
    rospy.loginfo(rospy.get_name() + " I heard %s", data.message)

# This ends up being the main while loop.
def listener():
    # Get the ~private namespace parameters from cd command line or launch file.
    topic = rospy.get_param('gps/fix', 'chatter')
    # Create a subscriber with appropriate topic, custom message and name of callback function.
    rospy.Subscriber(topic, String, callback)
    # Wait for messages on topic, go to callback function when new messages arrive.
    rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('gps_listener', anonymous = True)
    # Go to the main loop.
    listener()