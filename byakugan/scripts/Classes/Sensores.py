#!/usr/bin/env python

import rospy
import threading
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BotoesMsg

class Sensores:
    '''
    __refletancia
    __distancia
    __botoes
    __lock
    '''
    def __init__(self):
        self._lock = threading.Lock()

        self._lock.acquire()
        try:
            self._refletancia = RefletanciaMsg()
            self._distancia = SensoresDistanciaMsg()
            self._botoes = BotoesMsg()
        finally:
            self._lock.release()

    def setValues(self, refle, dist, btns):
        self._lock.acquire()
        try:
            self._refletancia = refle
            self._distancia = dist
            self._botoes = btns
        finally:
            self._lock.release()

    def getRefle(self, n):
        self._lock.acquire() #pega o lock
        try:
            return self._refletancia.refletancia[n] #le a variavel
        finally:
            self._lock.release() #solta o lock

    def getDist(self, n):
        self._lock.acquire() #pega o lock
        try:
            return self._distancia.sensoresDistancia[n] #le a variavel
        finally:
            self._lock.release() #solta o lock


    def getBtn1(self):
        self._lock.acquire()
        try:
            return self._botoes.botao1.data
        finally:
            self._lock.release()

    def getBtn2(self):
        self._lock.acquire()
        try:
            return self._botoes.botao2.data
        finally:
            self._lock.release()

    def getBtn3(self):
        self._lock.acquire()
        try:
            return self._botoes.botao3.data
        finally:
            self._lock.release()
