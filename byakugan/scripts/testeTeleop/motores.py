#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int32MultiArray
from byakugan.msg import CtrlMotores
import time

class Motores():
    def __init__(self):

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
        rospy.init_node("motores", anonymous=False)
        self.rate = rospy.Rate(20)

        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)


    def listener(self):
        rospy.Subscriber("est_motores", CtrlMotores, self.callback)
        rospy.spin()

    def callback(self, dataMotores):
        esq = dataMotores.esq.data
        dir = dataMotores.dir.data
        esqFrente = (esq == 1)
        dirFrente = (dir == 1)

        vel_default = (esq < 2 and dir < 2)

        delayPub = dataMotores.delay.data

        if vel_default:
            if not dataMotores.rampa.data:
                if esqFrente and dirFrente:
                    self.roboEmFrente(delayPub)
                elif dirFrente:
                    self.roboEsq(delayPub)
                elif esqFrente:
                    self.roboDir(delayPub)
                elif esq < 0 and dir < 0:
                    self.roboParaTras(delayPub)
                else:
                    self.roboParar(delayPub)
        else:
            self.roboAcionarMotores(esq, dir, delayPub)
        '''
        elif esqFrente and dirFrente:
            self.emFrenteRampa(delayPub)
        elif dirFrente:
            self.esquerdaRampa(delayPub)
        elif esqFrente:
            self.direitaRampa(delayPub)
        '''

    def pubDelayMotores(self, velEsq, velDir, delay):
        dataMotores = Int32MultiArray()
        tInicio = time.time()
        tAtual = tInicio

        iAnterior = -1

        while tAtual - tInicio < delay: #

            dataMotores.data = [velEsq, velDir]
            iAtual = int(tAtual - tInicio)
            if iAnterior != iAtual:
                iAnterior = iAtual
                self.pubMotores.publish(dataMotores)
                print iAtual
            tAtual = time.time()

        dataMotores.data = [0, 0]
        self.pubMotores.publish(dataMotores)

    # seguir linha
    def roboAcionarMotores(self, esq, dir, delay=0):
        self.pubDelayMotores(esq, dir, delay)

    def roboEmFrente(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_FRENTE, self.VEL_DIR_FRENTE, delay)
    def roboDir(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_FRENTE, self.VEL_DIR_TRAS, delay)
    def roboEsq(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_TRAS, self.VEL_DIR_FRENTE, delay)
    def roboParaTras(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_TRAS, self.VEL_DIR_TRAS, delay)
    def roboParar(self, delay=0):
        self.pubDelayMotores(0, 0, delay)

    '''
    # subir rampa
    def roboEmFrenteRampa(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_FRENTE_RAMPA, delay)
    def roboDirRampa(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_TRAS_RAMPA, delay)
    def roboEsqRampa(self, delay=0):
        self.pubDelayMotores(self.VEL_ESQ_TRAS_RAMPA, self.VEL_DIR_FRENTE_RAMPA, delay)
    '''

if __name__ == "__main__":
    motores = Motores()
    motores.roboEmFrente(5)
    #motores.listener()
