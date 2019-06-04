#!/usr/bin/env python

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import BoolStamped
def circular(img, circles):
	if (circles is not None):
		circles = np.uint16(np.around(circles))
		circulo.existe.data = True
		for i in circles[0, :]:
			x, y, r = i[0], i[1], i[2]

			center = (x, y)
			radius = r

			coordenadas.vector.x = x
			coordenadas.vector.y = y
			coordenadas.vector.z = r

			pub.publish(coordenadas)
	else:
		circulo.existe.data = False
		pub.publish(coordenadas)
	pub2.publish(circulo)
	return img

def acharCirculos(img):
	copiaImg = img.copy()

	cinza = cv2.cvtColor(copiaImg, cv2.COLOR_BGR2GRAY)
	cinza = cv2.medianBlur(cinza, 5)

	rows = cinza.shape[1]

 	circles = cv2.HoughCircles(cinza, cv2.HOUGH_GRADIENT, 1.2, rows/8,
 		param1=100, param2=30, minRadius=10, maxRadius=100)

	copiaImg = circular(copiaImg, circles)

	return copiaImg

def callback(data):
	ponte = CvBridge()
	imgCV = ponte.imgmsg_to_cv2(data,"bgr8")
	#imgCV = cv2.resize(imgCV, (400,400))

	imgCV = acharCirculos(imgCV)

def listenerImg():
	rospy.init_node('listenerCirculo', anonymous=True)
	rospy.Subscriber('topico_img', Image, callback)
	rospy.spin()

if __name__ == "__main__":
	pub = rospy.Publisher('coordenadas_circulos', Vector3Stamped, queue_size=10)
	pub2 = rospy.Publisher('tem_circulos', BoolStamped, queue_size=10)

	circulo = BoolStamped()
	coordenadas = Vector3Stamped()
	listenerImg()
