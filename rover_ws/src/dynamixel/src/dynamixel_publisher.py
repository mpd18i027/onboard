#!/usr/bin/env python 

import rospy
from std_msgs.msg import Float32MultiArray
import lib_robotis as lr
import math

class DynPub():
    def __init__(self):
        self.r_angles = Float32MultiArray()
        self.c_angles = Float32MultiArray()
        self.c_angles.data.append(0.0)
        self.c_angles.data.append(0.0)
        self.pub = rospy.Publisher('/dynamixel_feedback',Float32MultiArray,queue_size = 1)

        self.sub = rospy.Subscriber('dynamixel_command',Float32MultiArray,self.dynCallback)

    def dynCallback(self,msg):
        self.c_angles.data[0] = msg.data[0]
        self.c_angles.data[1] = msg.data[1]

if __name__ == "__main__":
    rospy.init_node('dynamixel_feedback_node',anonymous = True)
    hz = 60.0
    rate = rospy.Rate(hz)
    dynpub = DynPub()

    dynpub.r_angles.data.append(0.0)
    dynpub.r_angles.data.append(0.0)

    dyn = lr.USB2Dynamixel_Device('/dev/ttyUSB4',57600)
    flop = lr.Robotis_Servo(dyn, 2, series = 'MX')
    #flop = flop.write_address(0x0E, [255,3])
    twist = lr.Robotis_Servo(dyn, 1, series = 'MX')
    #twist = twist.write_address(0x0E, [255,3])
    # twist.multi_turn()

    while not rospy.is_shutdown():
        dynpub.r_angles.data[0] = flop.read_angle()#+15.0*math.pi/180.0
        dynpub.r_angles.data[1] = twist.read_angle()
        dynpub.pub.publish(dynpub.r_angles)
        flop.move_angle(dynpub.c_angles.data[0])
        twist.move_angle(dynpub.c_angles.data[1])

        rate.sleep()
