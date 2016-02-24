# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:38:18 2016

@author: ben
"""

import rospy
import cv2
<<<<<<< HEAD
import numpy
#import numpy as np
=======
import cv2.cv as cv
import numpy as np
from geometry_msgs.msg import Twist
>>>>>>> 4147749e67c2c786ac9a16e62a55946ef09c55d2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

trim = 60 #number of pixels to shave off, used to omit the turtlebot shelf from image
wheel_radius = 1
robot_radius = 1

mean_left = 0
mean_right = 0

 

class braitenberg_love:
    
    mean_left = 0
    mean_right = 0
    
    vel_limit = 0.4 #the maximum velocity that can be sent to a turtlebot
             
    def __init__(self):            
        cv2.namedWindow("Threshold left", 1)
        cv2.namedWindow("Threshold right")
        cv2.moveWindow('Threshold right', 425, 35)
        cv2.moveWindow('Threshold left', 35, 35)
        #cv2.namedWindow("Image feed")
        cv2.startWindowThread()
        self.bridge = CvBridge()
        #Used to access the simulated turtlebot's camera
        self.image_sub = rospy.Subscriber('/turtlebot_1/camera/rgb/image_raw',
                                          Image, self.callback)
<<<<<<< HEAD
        #Real robot
        #self.image_sub = rospy.Subscriber("/usb_cam/image_raw",
        #                                  Image, self.callback)
                                          
        self.pub = rospy.Publisher("/turtlebot_1/cmd_vel", Twist, queue_size=10)
        print 'INIT COMPLETE'
=======
        #self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",
        #                                  Image, self.callback)
        self.pub = rospy.Publisher('/turtlebot_1/cmd_vel', Twist, queue_size=10)
>>>>>>> 4147749e67c2c786ac9a16e62a55946ef09c55d2
                                          
    def callback(self, data):
            
<<<<<<< HEAD
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
            img_left = hsv_thresh[0:(height-trim), 0:(width/2)]
            img_right = hsv_thresh[0:(height-trim), (width/2):width]
            cv2.imshow('Threshold left', img_left)
            cv2.imshow('Threshold right', img_right)
            #cv2.imshow('Image feed', cv_image)
            self.mean_left = numpy.mean(img_left)
            self.mean_right = numpy.mean(img_right)
 
    def talker(self):
        while not rospy.is_shutdown():
            
            r = rospy.Rate(10)
            
            #Perform forward kinematics operation
            v, a = self.forward_kinematics(1 - (self.mean_right/15),1  - (self.mean_left/15))
            
            #Add results to a twist message
            twist_msg = Twist()
            twist_msg.linear.x = v
            twist_msg.angular.z = a
            
            #Limit velocities 
            if v > self.vel_limit:
                v = self.vel_limit
            if a > self.vel_limit:
                a = self.vel_limit    
            print 'Linear vel: ' + str(v) + ' Angular vel: ' + str(a) 
            #Publish velocities
            self.pub.publish(twist_msg)          
            r.sleep()
            
    def forward_kinematics(self, w_l, w_r):
        c_l = wheel_radius * w_l
        c_r = wheel_radius * w_r
        v = (c_l + c_r) / 2
        a = (c_l - c_r) / robot_radius
        return (v, a)   
            
rospy.init_node('braitenberg_love', anonymous=True)   
bl = braitenberg_love()
bl.talker()
rospy.spin()
=======
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
>>>>>>> 4147749e67c2c786ac9a16e62a55946ef09c55d2
cv2.destroyAllWindows()