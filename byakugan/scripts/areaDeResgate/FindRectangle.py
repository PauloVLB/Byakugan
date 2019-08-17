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

        #rospy.init_node('find_rectangle', anonymous=False)

        self.img = None
        self.thresh = None

        #self.CENTER_WINDOW = (240/2), (320/2)

    def callback(self, imgCompressed):
        np_arr = np.fromstring(imgCompressed.data, np.uint8)
    	self.img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    	self.img = cv2.flip(self.img, 2)
        self.find()
        self.showImg()

    def cookImg(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5) # interfere?
        gray = 255 - gray

        _, self.thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        _, contours, _= cv2.findContours(self.thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        return contours

    def find(self):
        try:
            contours = self.cookImg()
            self.drawRectangle(contours[len(contours) - 1], 10) # draw contorno da própria img
            contours = self.cookImg() # cozinha a img novamente separando possíveis contours colados na img inicial

            for i in range(0, len(contours) - 1): # -1 impede de draw contour da propria img

                cnt = contours[i]

                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)

                cX, cY = self.getCentroid(cnt, self.img) # pega centro do contorno
                #print cX, cY

                area = self.getArea(cnt)
                #print area

                # aproxima pontos do contorno - corners
                approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
                print approx.ravel()

                if self.isBigDist(approx): # verifica se o contorno é retangulo
                    # draw centro do contorno e retangulo no contorno
                    self.drawCentroid(cX, cY)
                    self.drawRectangle(cnt, 6)

        except: # ???
            print 'error in img'

    def showImg(self):
        cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
        cv2.imshow('thresh', self.thresh)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.imshow('result', self.img)
        cv2.waitKey(0)

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

        #print diferenca

        return diferenca > 20 # if true é retangulo else bola preta

    def drawCentroid(self, cX, cY):
        cv2.circle(self.img, (cX, cY), 10, (0, 255, 0), -1)

    def drawRectangle(self, cnt, width):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(self.img,[box],0,(0,255, 0), width)

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
    fr.img = cv2.imread('c3v2i1.png', 1)
    #img = cv2.imread('c1v2i1.png', 1)
    fr.find()
    fr.showImg()
