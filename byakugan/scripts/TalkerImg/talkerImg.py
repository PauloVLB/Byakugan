#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def talkerImg():
	pub = rospy.Publisher('topico_img', Image, queue_size=10)
	rospy.init_node('talkerImg', anonymous=True)
	rate = rospy.Rate(10)

	ponte = CvBridge()
	camera = cv2.VideoCapture(0)
	rval = True

	while rval and not rospy.is_shutdown():
		rval, imgCV = camera.read()
		imgCV = cv2.flip(imgCV, 2)
		imgMsg = ponte.cv2_to_imgmsg(imgCV, "bgr8")
		pub.publish(imgMsg)

		rate.sleep()


if __name__ == "__main__":
	try:
		talkerImg()
	except rospy.ROSInterruptException:
		pass