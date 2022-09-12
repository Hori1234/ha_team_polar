#!/usr/bin/env python3

# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Willow Garage, Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import rospy
from polar_control.msg import CustomMsg
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

MAX_WHEEL_VEL = 100
MAX_RIGHT_VEL = 100


LIN_VEL_STEP_SIZE = 2


msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
   w    e
   s    d  f
   
w/s : increase/decrease left wheel velocity by 2
e/d : increase/decrease right wheel velocity by 2
space key, s : force stop
CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      if sys.version_info[0] >= 3:
        return msvcrt.getch().decode()
      else:
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_left_vel, target_right_vel):
    return "currently:\tleft vel %s\t right vel %s " % (target_left_vel,target_right_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel, -MAX_WHEEL_VEL, MAX_WHEEL_VEL)

    return vel



if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('polar_prototype_key_teleop')
    pub = rospy.Publisher('polar_prototype/cmd_drive', CustomMsg, queue_size=10)


    status = 0
    target_left_vel   = 0.0
    target_right_vel  = 0.0
    control_left_vel  = 0.0
    control_right_vel = 0.0

    
    print(msg)
    while(1):
        key = getKey()
        if key == 'w' :
            target_left_vel = checkLinearLimitVelocity(target_left_vel + LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_left_vel,target_right_vel))
        elif key == 's' :
            target_left_vel = checkLinearLimitVelocity(target_left_vel - LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_left_vel,target_right_vel))
        elif key == 'e' :
            target_right_vel = checkLinearLimitVelocity(target_right_vel + LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_left_vel,target_right_vel))
        elif key == 'd' :
            target_right_vel = checkLinearLimitVelocity(target_right_vel - LIN_VEL_STEP_SIZE)
            status = status + 1
            print(vels(target_left_vel,target_right_vel))
        elif key == ' ' or key == 'f' :
            target_linear_vel   = 0.0
            control_linear_vel  = 0.0
            target_angular_vel  = 0.0
            control_angular_vel = 0.0
            print(vels(target_linear_vel, target_angular_vel))
        else:
            if (key == '\x03'):
                break

        if status == 20 :
            print(msg)
            status = 0

        output_msg = CustomMsg()

        #control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
        #twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

        #control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
        #twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel
        output_msg.drive.left_vel = target_left_vel
        output_msg.drive.right_vel = target_right_vel
        pub.publish(output_msg)


    # finally:
    #     output_msg = CustomMsg()
    #     output_msg.drive.left_vel  = 0.0
    #     output_msg.drive.right_vel = 0.0
    #     pub.publish(output_msg)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)