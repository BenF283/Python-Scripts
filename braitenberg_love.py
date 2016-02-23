# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:38:18 2016

@author: ben
"""

import rospy
import math
import cv2
import cv2.cv as cv
import numpy as np
from geometry_msgs.msg import Twist

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class braitenberg_love:
            
    def __init__(self):            
        cv2.namedWindow("Image feed", 1)
        cv2.startWindowThread()
        self.bridge = CvBridge()
        #Used to access the simulated turtlebot's camera
        self.image_sub = rospy.Subscriber('/turtlebot_1/camera/rgb/image_raw',
                                          Image, self.callback)
        #self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",
        #                                  Image, self.callback)
        self.pub = rospy.Publisher('/turtlebot_1/cmd_vel', Twist, queue_size=10)
                                          
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e
            
        cv2.imshow('Image feed', cv_image)

    def move(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            twist_msg = Twist()            
            twist_msg.linear.x = 1.0
            self.pub.publish(twist_msg)
            r.sleep()
        
if __name__ == '__main__':
    rospy.init_node('braitenberg_love', anonymous=True)
    bl = braitenberg_love()
    bl.move()
    rospy.spin()
cv2.destroyAllWindows()