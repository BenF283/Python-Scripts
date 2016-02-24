# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:53:04 2016

Shows split vision from RBG camera based on HSV intensitiy values

@author: ben
"""


import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist


class vision_hsvsplit:
    

    trim = 60
             
    def __init__(self):            
        cv2.namedWindow("Threshold left", 1)
        cv2.namedWindow("Threshold right")
        cv2.namedWindow("Image feed")
        cv2.startWindowThread()
        self.bridge = CvBridge()
        #Used to access the simulated turtlebot's camera
        self.image_sub = rospy.Subscriber("/turtlebot_1/camera/rgb/image_raw",
                                          Image, self.callback)
        #Real robot
        #self.image_sub = rospy.Subscriber("/usb_cam/image_raw",
        #                                  Image, self.callback)
                                          
        self.pub = rospy.Publisher("/turtlebot_1/cmd_vel", Twist, queue_size=10)
                                          
    def callback(self, data):
            
            try:
                cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            except CvBridgeError, e:
                print e
            hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            height, width, channels = hsv_img.shape        
    
            hsv_thresh = cv2.inRange(hsv_img,
                                     numpy.array((0, 0, 0)),
                                     numpy.array((255, 20, 40)))
            #Split the thresholds into two seperate images
            img_left = hsv_thresh[0:(height-self.trim), 0:(width/2)]
            img_right = hsv_thresh[0:(height-self.trim), (width/2):width]
            cv2.imshow('Threshold left', img_left)
            cv2.imshow('Threshold right', img_right)
            cv2.imshow('Image feed', cv_image)
            
rospy.init_node('vision_hsvsplit', anonymous=True)   
vision_hsvsplit()
rospy.spin()
cv2.destroyAllWindows()