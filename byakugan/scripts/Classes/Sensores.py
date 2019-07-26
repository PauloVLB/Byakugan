#!/usr/bin/env python

import rospy
import message_filters
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolStamped, BotoesMsg

class Sensores:
    __refletancia
    __distancia
    __botoes
    lock
    lockRefle = []
    lockDist = []
    lockBtns = []

    def __init__(self):
        self.__refletancia = RefletanciaMsg()
        self.__distancia = SensoresDistanMsg()
        self.__botoes = BotoesMsg()

    def setValues(self, refle, dist, btns):
        global lock
        lock.aquire()

        self.__refletancia = refle
        self.__distancia = dist
        self.__botoes = btns

        lock.release()

    def getRefle(self, n):
        global lockRefle
        lockRefle[n].acquire() #pega o lock de determinada variável de refletancia

        refleValue = self.__refletancia.refletancia[n] #lê a variável

        lockRefle[n].release() #solta o lock
        return refleValue

    def getDist(self, n):
        global lockDist
        lockDist[n].acquire() #pega o lock de determinada variável de distancia

        distValue = self.__distancia.sensoresDistancia[n] #lê a variável

        lockDist[n].release() #solta o lock
        return distValue

    def getBtn1(self):
        global lockBtns
        lockBtns[0].acquire()

        btn1Value = self.__botoes.botao1.data

        lockBtns[0].release()
        return btn1Value

    def getBtn2(self):
        global lockBtns
        lockBtns[1].acquire()

        btn2Value = self.__botoes.botao2.data

        lockBtns[1].release()
        return btn2Value

    def getBtn3(self):
        global lockBtns
        lockBtns[2].acquire()

        btn3Value = self.__botoes.botao3.data

        lockBtns[2].release()
        return btn3Value
