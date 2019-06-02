#!/usr/bin/env python
#identificador.py

import cv2
from cv_bridge import CvBridge

class Detect():
	def __init__ (self, imgMsg):
		self.caminho = '/opt/ros/kinetic/share/OpenCV-3.3.1-dev/'
		self.imgMsg = imgMsg

		ponte = CvBridge()
		self.imgCV = ponte.imgmsg_to_cv2(self.imgMsg, "bgr8")

	def elementos_face(self, cascade, sf=1.2, mn=5):	
		copiaImg = self.imgCV.copy()
		cinza = cv2.cvtColor(copiaImg, cv2.COLOR_BGR2GRAY)

		detector = cv2.CascadeClassifier(self.caminho + cascade)
		elementos = detector.detectMultiScale(cinza, scaleFactor=sf, minNeighbors=mn)

		return elementos

class Draw():
	def circular(self, img, objeto, txt='detectado_', cor=(0,255,0), expe=3, cont=1):
		for (x,y,w,h) in objeto:
			cv2.circle(img, (x+(w/2), y+(h/2)), (w/2), cor, expe)
			cv2.putText(img, txt + str(cont), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, cor, 2)
			cont += 1

		return img

	def circular(self, img, arrayCoordenadas, txt='detectado_', cor=(0,255,0), expe=3, cont=1):
		x = int(arrayCoordenadas[0])
		y = int(arrayCoordenadas[1])
		w = int(arrayCoordenadas[2])
		h = int(arrayCoordenadas[3])

		cv2.circle(img, (x+(w/2), y+(h/2)), (w/2), cor, expe)
		cv2.putText(img, txt + str(cont), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, cor, 2)
		cont += 1

		return img



		
