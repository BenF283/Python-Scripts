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

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class braitenberg_love:
            
    def __init__(self):            
        cv2.namedWindow("Image feed", 1)
        cv2.startWindowThread()
        self.bridge = CvBridge()
        #Used to access the simulated turtlebot's camera
        self.image_sub = rospy.Subscriber("/turtlebot_1/camera/rgb/image_raw",
                                          Image, self.callback)
                                          
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e
            
        cv2.imshow('Image feed', cv_image)

braitenberg_love()
rospy.init_node('braitenberg_love', anonymous=True)
rospy.spin()
cv2.destroyAllWindows()