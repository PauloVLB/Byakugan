#!/usr/bin/env python

import rospy
import threading
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import BoolStamped

class Camera:
    def __init__(self):
        self.__lock = threading.Lock()

        self.__lock.acquire()
        try:
            self.__coordenadas = Vector3Stamped()
            self.__vitima = BoolStamped()
        finally:
            self.__lock.release()
    
    def setValues(self, coordenadas, vitima):
        self.__lock.acquire()
        try:
            self.__coordenadas = coordenadas
            self.__vitima = vitima
        finally:
            self.__lock.release()
    
    def getCoordenadasVitima():
        self.__lock.acquire()
        try:
            return self.__coordenadas
        finally
            self.__lock.release()
    
    def getVitima():
        self.__lock.acquire()
        try:
            return self.__vitima
        finally
            self.__lock.release()
    