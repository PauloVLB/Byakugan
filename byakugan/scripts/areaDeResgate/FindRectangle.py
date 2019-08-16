#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
#from byakugan.msg import CentroidObject
from sensor_msgs.msg import CompressedImage

class FindRectangle:
    def __init__(self):
        #self.pub = rospy.Publisher('centroid_rectangle', CentroidObject, queue_size=10, latch=True)

        rospy.init_node('find_rectangle', anonymous=False)
        self.thresh = None

        #self.CENTER_WINDOW = (240/2), (320/2)

    def callback(self, imgCompressed):
        np_arr = np.fromstring(imgCompressed.data, np.uint8)
    	imgCV = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    	imgCV = cv2.flip(imgCV, 2)
        self.find(imgCV)

        #cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        #cv2.imshow('thresh', self.thresh)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.imshow('result', imgCV)
        cv2.waitKey(1)

    def find(self, imgCV):
        try:
            gray = cv2.cvtColor(imgCV, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5) # interfere?
            gray = 255 - gray

            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
            _, contours, _= cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours: # iteração com cada contorno encontrado
                cX, cY = self.getCentroid(cnt, imgCV) # pega centro do contorno

                #print cX, cY
                area = self.getArea(cnt)

                # aproxima pontos do contorno - corners
                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)

                if not area > 50000.0 and area > 1000: # gambiarra
                    if self.isBigDist(approx): # verifica se o contorno é retangulo
                        # draw centro do contorno e retangulo no contorno
                        self.drawCentroid(cX, cY, imgCV)
                        self.drawRectangle(cnt, imgCV)
        except: # ???
            print 'error in img'

    def isBigDist(self, approx):
        approxRavel = approx.ravel() # transforma em um vetor
        points = []
        pointsX = []
        pointsY = []
        for i in range(0, len(approxRavel) - 1, 2): # vai adicionando os pontos do contorno
            x  = approxRavel[i]
            y  = approxRavel[i + 1]
            pointsX.append(x) # vai ser usado para saber o comprimento dos pontos
            pointsY.append(y) # vai ser usado para saber o altura dos pontos
            points.append((x,y)) # pontos do objeto

        xInicial = min(pointsX)
        xFinal = max(pointsX)
        yInicial = min(pointsY)
        yFinal = max(pointsY)

        compX = abs(xFinal - xInicial)
        compY = abs(yFinal - yInicial)

        diferenca = abs(compX - compY)

        return diferenca > 50 # if true é retangulo

    def drawCentroid(self, cX, cY, imgCV):
        cv2.circle(imgCV, (cX, cY), 5, (0, 255, 0), -1)

    def drawRectangle(self, cnt, imgCV):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(imgCV,[box],0,(0,255, 0),2)

    def getArea(self, cnt): return cv2.contourArea(cnt)

    def listenerImg(self):
    	rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, self.callback)
    	rospy.spin()

    def getCentroid(self, cnt, imgCV):
        M = cv2.moments(cnt)
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY

if __name__ == "__main__":
    fr = FindRectangle()
    fr.listenerImg()
