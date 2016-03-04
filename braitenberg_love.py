# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:38:18 2016

A script implementing the braitenberg love robot design. Additional code has
been added to prevent collisions with walls and other objects

@author: ben
"""

import rospy
import cv2
import numpy
#import numpy as np

from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
 

class braitenberg_love:
    
    #Initialise the sensor values
    mean_left = 0.0
    mean_right = 0.0
    
    #Set some maximum velocities so we don't race the bots
    vel_linear_limit = 0.6 
    vel_angular_limit = 0.8

    #define robot dimensions
    wheel_radius = 1
    robot_radius = 1
    
    #number of pixels to shave off, used to omit the turtlebot shelf from image
    trim = 60 

    #Initialise depth value
    center_depth = 0.0
             
    def __init__(self):

        #Set up imaging windows            
        cv2.namedWindow("Threshold left", 1)
        cv2.namedWindow("Threshold right")
        cv2.namedWindow("Image feed")
        
        #Move them just to make running the program simpler
        cv2.moveWindow('Threshold right', 425, 35)
        cv2.moveWindow('Threshold left', 35, 35)
        cv2.moveWindow('Image feed', 815, 35)

        cv2.startWindowThread()
        self.bridge = CvBridge()
        
        #Camera Subscriber
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",
                                          Image, self.imaging_callback)
        #Real robot
        #self.image_sub = rospy.Subscriber("/usb_cam/image_raw",
        #                                  Image, self.callback)

        #Scan subscriber        
        self.depth_sub = rospy.Subscriber("/scan",
                                          LaserScan, self.depth_callback)
        #Publisher for velocities
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
                                          
    def imaging_callback(self, data):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e
        
        hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        height, width, channels = hsv_img.shape        

        hsv_thresh = cv2.inRange(hsv_img,
                                 numpy.array((0, 80, 0)),
                                 numpy.array((8, 255, 255)))
        #Split the thresholds into two seperate images
        img_left = hsv_thresh[0:(height-self.trim), 0:(width/2)]
        img_right = hsv_thresh[0:(height-self.trim), (width/2):width]
        
        #Show images to windows
        cv2.imshow('Threshold left', img_left)
        cv2.imshow('Threshold right', img_right)
        cv2.imshow('Image feed', cv_image)

        #Calculate and store the mean
        self.mean_left = numpy.mean(img_left)
        self.mean_right = numpy.mean(img_right)
 
    def depth_callback(self, data):
        self.center_depth = data.ranges[len(data.ranges)/2]
        #self.center_depth = numpy.mean(data.ranges)
        
            
    def talker(self):
        while not rospy.is_shutdown():            
            r = rospy.Rate(10)
            msg = ""
            #Perform forward kinematics operation
            v, a = self.forward_kinematics(1 - (self.mean_right/255),1  - (self.mean_left/255))
            print self.mean_left
            print self.mean_right
            
            
            #Create a twist message
            twist_msg = Twist()
            
            #Check if turtlebot is close to an object, if it's the "loved" object then stop.
            if self.center_depth < 1.5 and (self.mean_right + self.mean_left) / 2 > 10:
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                msg = "Close to loved object"
            #If it's something else (i.e a wall/obstruction), try moving in a 
            #different direction
            elif self.center_depth < 1.5:
                twist_msg.angular.z = self.vel_angular_limit
                msg = "Close to wall, rotating"
            #Otherwise continue with sensor values
            else:
                msg = ""
                
                #This block of if statements is just to prevent the turtlebot
                #moving at ridiculous speeds
                if v > self.vel_linear_limit:
                    v = self.vel_linear_limit
                    msg = msg + "Linear velocity limited. "
                if a > self.vel_angular_limit:
                    msg = msg + "Angular velocity limited. "
                    a = self.vel_angular_limit   
                
                #Add the values to the twist message
                twist_msg.linear.x = v
                twist_msg.angular.z = a
                msg = "Moving..."

            #Publish!
            print 
            self.pub.publish(twist_msg)
            print msg
            r.sleep()
    
    #Code to convert the velocities 
    def forward_kinematics(self, w_l, w_r):
        c_l = self.wheel_radius * w_l
        c_r = self.wheel_radius * w_r
        v = (c_l + c_r) / 2
        a = (c_l - c_r) / self.robot_radius
        return (v, a)   

#Initialise a new node for our code           
rospy.init_node('braitenberg_love', anonymous=True)   
bl = braitenberg_love()
bl.talker()
rospy.spin()
cv2.destroyAllWindows()