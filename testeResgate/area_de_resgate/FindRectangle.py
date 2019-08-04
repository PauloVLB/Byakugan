#!/usr/bin/env python

import numpy as np
import cv2

font = cv2.FONT_HERSHEY_COMPLEX
THRESH = 80 # se aparecer muitos pontos, diminua esse cara
EPSILION = 0.01 # define o raio do approx

ext = ".jpg"
arquivo = "visao1"

img = cv2.imread("simulador/" + arquivo + ext, cv2.IMREAD_GRAYSCALE)
img = cv2.bilateralFilter(img, 2, 50, 200)
# THRESH - 255 > aquelas cores que serao convertidas em binario
# limites identificados sao transformados em binario - preto e branco
_, threshold = cv2.threshold(img, THRESH, 255, cv2.THRESH_BINARY)

_, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # approx utilizado para impedir imperfeicoes nos cnts
    approx = cv2.approxPolyDP(cnt, EPSILION*cv2.arcLength(cnt, True), True)

    # (x, y) ponto inicial do objeto
    x = approx.ravel()[0] # pega primeira posicao x do approx
    y = approx.ravel()[1] # pega primeira posicao y do approx

    bugRec = x == 0 and y == 0
    if not bugRec: # evita contornar a propria img
        cv2.drawContours(img, [approx], 0, (0), 5)

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
                cv2.putText(img, "Rectangle", (x, y), font, 1, (0))

            print 'points ' + str(points)
            print 'x_raio ' + str(x_raio)
            print 'approxRavel ', approxRavel

cv2.imshow("threshold", threshold)
cv2.imshow("shapes", img)

k = cv2.waitKey(0)
while cv2.waitKey(1) != ord('x'):
    pass
if k == ord('s'):
    cv2.imwrite('resultSimulador/' + arquivo + '_result' + ext, img)
    print 'saved'

cv2.destroyAllWindows()
