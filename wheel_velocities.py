#!/usr/bin/env python
#Week 3
import rospy
#import cv2
import math
#import cv2.cv as cv
import numpy as np
#from sensor_msgs.msg import Image
from std_msgs.msg import Float32
#from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

wheel_radius = 1.0
robot_radius = 1.0


class wheel_velocities:
   
    def __init__(self):

        #Used to access the simulated turtlebot's camera
        self.wheel_sub = rospy.Subscriber("/turtlebot_1/wheel_vel_left",
                                          Float32, self.callback)  
                                           
        #Used for the real turtlebot                                  
        #self.wheel_sub = rospy.Subscriber("/wheel_vel_left",
        #                                  Image, self.callback)
        self.pub = rospy.Publisher("/turtlebot_1/cmd_vel", Twist, queue_size=10)

    def callback(self, data):
        wheel_left = forward_kinematics(float(data), 0.0)
        print data
        r = rospy.rate(10)
        while not rospy.is_shutdown():
            twist_msg = Twist()
            
            twist_msg.angular.x = wheel_left[0]
            self.pub.publish(twist_msg)        
            r.sleep()
       
def forward_kinematics(w_l, w_r):
    c_l = wheel_radius * w_l
    c_r = wheel_radius * w_r
    v = (c_l + c_r) / 2
    a = (c_l - c_r) / robot_radius
    return (v, a)
     
wheel_velocities()
rospy.init_node('wheel_velocities', anonymous=True)
rospy.spin()
