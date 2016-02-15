#!/usr/bin/env python
#Week 3
import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String


class image_converter:

    def __init__(self):


        cv2.namedWindow("canny_image", 1)
        cv2.startWindowThread()
        self.bridge = CvBridge()
        #Used to access the simulated turtlebot's camera
        self.image_sub = rospy.Subscriber("/turtlebot_1/camera/rgb/image_raw",
                                          Image, self.callback)
        #Used for the real turtlebot                                  
        #self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",
        #                                  Image, self.callback)

    def callback(self, data):       
            try:
                cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            except CvBridgeError, e:
                print e
                    
                    #Create publisher
            pub = rospy.Publisher('/turtlebot_1/result_topic', String, queue_size=10)
            img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
            img = cv2.medianBlur(img,5)
                    
            #Apply canny edge detection
            canny_image = cv2.Canny(img, 10, 200)

            r = rospy.Rate(10)
       
            #Calculate mean        
            mean_intensity = numpy.mean(canny_image)
            print(mean_intensity)
            #Publish mean to result_topic
            pub.publish(mean_intensity)
            r.sleep()
            cv2.imshow('canny_image',canny_image)
            
image_converter()
rospy.init_node('image_converter', anonymous=True)
rospy.spin()
cv2.destroyAllWindows()