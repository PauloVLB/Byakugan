#!/usr/bin/env python

import rospy
import message_filters
import threading
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolStamped, BotoesMsg

class Sensores:
    '''
    __refletancia
    __distancia
    __botoes
    __lock
    __lockRefle = []
    __lockDist = []
    __lockBtns = []
    '''
    def __init__(self, nRefle=4, nDist=3, nBtns=3):
        self.__refletancia = RefletanciaMsg()
        self.__distancia = SensoresDistanMsg()
        self.__botoes = BotoesMsg()

        self.__lock = threading.Lock()
        self.__lockRefle = [threading.Lock()] * nRefle
        self.__lockDist = [threading.Lock()] * nDist
        self.__lockBtns = [threading.Lock()] * nBtns

    def setValues(self, refle, dist, btns):
        self.__lock.aquire()

        self.__refletancia = refle
        self.__distancia = dist
        self.__botoes = btns

        self.__lock.release()

    def getRefle(self, n):
        self.__lockRefle[n].acquire() #pega o lock de determinada variável de refletancia

        refleValue = self.__refletancia.refletancia[n] #lê a variável

        self.__lockRefle[n].release() #solta o lock
        return refleValue

    def getDist(self, n):
        self.__lockDist[n].acquire() #pega o lock de determinada variável de distancia

        distValue = self.__distancia.sensoresDistancia[n] #lê a variável

        self.__lockDist[n].release() #solta o lock
        return distValue

    def getBtn1(self):
        self.__lockBtns[0].acquire()

        btn1Value = self.__botoes.botao1.data

        self.__lockBtns[0].release()
        return btn1Value

    def getBtn2(self):
        self.__lockBtns[1].acquire()

        btn2Value = self.__botoes.botao2.data

        self.__lockBtns[1].release()
        return btn2Value

    def getBtn3(self):
        self.__lockBtns[2].acquire()

        btn3Value = self.__botoes.botao3.data

        self.__lockBtns[2].release()
        return btn3Value
