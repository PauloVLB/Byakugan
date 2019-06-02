#!/usr/bin/env python
import rospy
import cv2
import message_filters
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from identificador import Draw

def callbackCoordenadas(data):
	arrayCoordenadas.data = data.data

def callbackImg(data):
	imgCV = ponte.imgmsg_to_cv2(data, "bgr8")

	d.circular(imgCV, arrayCoordenadas.data, 'Face_')

	cv2.namedWindow('FACES', cv2.WINDOW_NORMAL)
	cv2.imshow('FACES', imgCV)
	cv2.waitKey(1)


def listenerCoordenadas():
	rospy.init_node('showFaces', anonymous=True)
	
	subCoordenadas = message_filters.Subscriber('coordenadas_detectadas', Float64MultiArray)
	subCoordenadas.registerCallback(callbackCoordenadas)
	
	subImg = message_filters.Subscriber('topico_img', Image)
	subImg.registerCallback(callbackImg)

	rospy.spin()

if __name__ == '__main__':
	arrayCoordenadas = Float64MultiArray()
	arrayCoordenadas.data = [0,0,0,0]
	ponte = CvBridge()
	d = Draw()

	listenerCoordenadas()