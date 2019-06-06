#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int32MultiArray
from byakugan.msg import CtrlMotores
import time

class Motores():
    def __init__(self):

        rospy.init_node("motores", anonymous=False)

        self.VEL_DIR_FRENTE_RAMPA = 88
        self.VEL_DIR_TRAS_RAMPA = 68

        self.VEL_ESQ_FRENTE_RAMPA = 85
        self.VEL_ESQ_TRAS_RAMPA = 65

        self.VEL_DIR_FRENTE = 48
        self.VEL_DIR_TRAS = -48

        self.VEL_ESQ_FRENTE = 45
        self.VEL_ESQ_TRAS = -45

        self.dataMotores = Int32MultiArray()

        # publisher
        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)

    def listener(self):
        rospy.Subscriber("est_motores", CtrlMotores, self.callback)
        rospy.spin()
    def callback(self, dataMotores):
        esq = dataMotores.esq
        dir = dataMotores.dir
        esqFrente = (esq == 1)
        dirFrente = (dir == 1)

        delayPub = dataMotores.delay

        if not dataMotores.rampa:
            if esqFrente and dirFrente:
                self.emFrente(delayPub)
            elif dirFrente:
                self.esquerda(delayPub)
            elif esqFrente:
                self.direita(delayPub)
            elif esq < 0 and dir < 0:
                self.paraTras(delayPub)
            else:
                self.parar(delayPub)
        '''
        elif esqFrente and dirFrente:
            self.emFrenteRampa(delayPub)
        elif dirFrente:
            self.esquerdaRampa(delayPub)
        elif esqFrente:
            self.direitaRampa(delayPub)
        '''

    def pubDelayMotores(self, delay):
        tInicio = time.time()
        tAtual = time.time()
        while tAtual - tInicio <= delay: # TESTAR
            self.pubMotores(self.dataMotores)
            tAtual = time.time()

    # seguir linha
    def roboEmFrente(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_FRENTE, self.VEL_DIR_FRENTE]
        self.pubDelayMotores(delay)
    def roboDir(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_FRENTE, self.VEL_DIR_TRAS]
        self.pubDelayMotores(delay)
    def roboEsq(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_TRAS, self.VEL_DIR_FRENTE]
        self.pubDelayMotores(delay)
    def roboParaTras(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_TRAS, self.VEL_DIR_TRAS]
        self.pubDelayMotores(delay)
    def roboParar(self, delay=0):
        self.dataMotores = [0, 0]
        self.pubDelayMotores(delay)

    '''
    # subir rampa
    def roboEmFrenteRampa(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_FRENTE_RAMPA]
        self.pubDelayMotores(delay)
    def roboDirRampa(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_TRAS_RAMPA]
        self.pubDelayMotores(delay)
    def roboEsqRampa(self, delay=0):
        self.dataMotores = [self.VEL_ESQ_TRAS_RAMPA, self.VEL_DIR_FRENTE_RAMPA]
        self.pubDelayMotores(delay)
    '''

if __name__ == "__main__":
    motores = Motores()
    motores.listener()
