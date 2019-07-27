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
    '''
    def __init__(self):
        self.__lock = threading.Lock()

        self.__lock.acquire()
        try:
            self.__refletancia = RefletanciaMsg()
            self.__distancia = SensoresDistanMsg()
            self.__botoes = BotoesMsg() 
        finally:
            self.__lock.release()

    def setValues(self, refle, dist, btns):
        self.__lock.acquire()
        try:
            self.__refletancia = refle
            self.__distancia = dist
            self.__botoes = btns
        finally:
            self.__lock.release()

    def getRefle(self, n):
        self.__lock.acquire() #pega o lock
        try:
            return self.__refletancia.refletancia[n] #lê a variável
        finally:
            self.__lock.release() #solta o lock

    def getDist(self, n):
        self.__lock.acquire() #pega o lock
        try:
            return self.__distancia.sensoresDistancia[n] #lê a variável
        finally:
            self.__lock.release() #solta o lock


    def getBtn1(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao1.data
        finally:
            self.__lock.release()

    def getBtn2(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao2.data
        finally:
            self.__lock.release()

    def getBtn3(self):
        self.__lock.acquire()
        try:
            return self.__botoes.botao3.data
        finally:
            self.__lock.release()
