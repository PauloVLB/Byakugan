#!/usr/bin/env python

import numpy as np
import cv2

class FindRectangle():

    def nothing(self):
        pass

    def __init__(self, thresh=80, epsilion=0.01):
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.THRESH = thresh # define espectro de cor minimo a ser "thresholdado"
        self.EPSILION = epsilion # define o raio do approx

        self.img = None
        self.threshold = None
        self.contours = None


        self.backTrackbar = np.zeros((300,512,3), np.uint8)
        self.trackbar = cv2.namedWindow('trackbar')

        cv2.createTrackbar('THRESH','image',0,255, self.nothing)
        cv2.createTrackbar('EPSILION','image',0,255, self.nothing)


    def setContours(self):
        _, self.contours, _ = cv2.findContours(self.threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def setThreshold(self):
        _, self.threshold = cv2.threshold(self.img, self.THRESH, 255, cv2.THRESH_BINARY)

    def cookImg(self, img):
        if not img is None:
            self.img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            self.img = cv2.bilateralFilter(self.img, 2, 50, 200) # ajuda a suavizar img

            self.setThreshold()
            self.setContours()
        else:
            print 'setImg none'


    def imshowRectangles(self, img):

        self.cookImg(img)

        for cnt in self.contours:
            # approx utilizado para impedir imperfeicoes nos cnts
            approx = cv2.approxPolyDP(cnt, self.EPSILION*cv2.arcLength(cnt, True), True)

            # (x, y) ponto inicial do objeto
            x = approx.ravel()[0] # pega primeira posicao x do approx
            y = approx.ravel()[1] # pega primeira posicao y do approx

            bugRec = x == 0 and y == 0

            if not bugRec: # evita contornar a propria img
                cv2.drawContours(self.img, [approx], 0, (0), 5)

                points = len(approx)
                approxRavel = approx.ravel()

                if points == 4 or points == 5:
                    if points == 4:
                        x_max = approxRavel[4]
                        x_raio = abs(x_max - x) # abs resolve rectangles ao contrario
                    elif points == 5:
                        x_max = approxRavel[5]
                        x_raio = abs(x_max - x) # abs resolve rectangles ao contrario

                    if abs(x_raio) > 100: # evita retangulos muito finos
                        cv2.putText(self.img, "Rectangle", (x, y), self.font, 1, (0))

                    print 'points ' + str(points)
                    print 'x_raio ' + str(x_raio)
                    print 'approxRavel ', approxRavel

        cv2.imshow("threshold", self.threshold)
        cv2.imshow("result", self.img)

        print 'press x to stop'
        while not cv2.waitKey(1) == ord('x'):
            pass

        cv2.destroyAllWindows()

    def trackbar(self):

        cv2.imshow('trackbar', self.backTrackbar)

        print 'press x to stop'
        while not cv2.waitKey(1) == ord('x'):
            pass

        cv2.destroyAllWindows()

if __name__ == "__main__":
    fr = FindRectangle()
    img = cv2.imread('simulador/visao8.jpg', 1)
    #fr.imshowRectangles(img)
    fr.trackbar()
