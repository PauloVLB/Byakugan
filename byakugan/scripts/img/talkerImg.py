#!/usr/bin/env python
import rospy 
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class TalkerImg:
	def __init__(self):
		rospy.init_node("talkerCamImg", anonymous=False)
		rospy.loginfo("Starting node " + rospy.get_name())

		self.camera = cv2.VideoCapture(0)
		
		
		self.pubImg = rospy.Publisher("imgCam", Image, queue_size=10)
		self.bridge = CvBridge()
		
		self.rate = rospy.Rate(20)
		
		self.pub()

	def pub(self):
		rospy.loginfo("Publishing cam image")
		while not rospy.is_shutdown():
			_, frame = self.camera.read()
			frame = cv2.resize(frame, (320,240))

			imgMsg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
			self.pubImg.publish(imgMsg)
			
			self.rate.sleep()
		

if __name__ == "__main__":
	ros_node = TalkerImg()
	rospy.spin()