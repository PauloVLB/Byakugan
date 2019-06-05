#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int32MultiArray
from byakugan.msg import CtrlMotores

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

        self.listener() ''' inicia o loop '''

    def listener():
        rospy.Subscriber("est_motores", CtrlMotores, callback)
        rospy.spin()
    def callback(dataMotores):
        esq = dataMotores.esq
        dir = dataMotores.dir
        esqFrente = (esq == 1)
        dirFrente = (dir == 1)

        delayPub = dataMotores.delay

        if not dataMotores.rampa:
            if esqFrente and dirFrente:
                self.emFrente()
            elif dirFrente:
                self.esquerda()
            elif esqFrente:
                self.direita()
            elif esq < 0 and dir < 0:
                self.paraTras()
            else:
                self.parar()
        elif esqFrente and dirFrente:
            self.emFrenteRampa()
        elif dirFrente:
            self.esquerdaRampa()
        elif esqFrente:
            self.direitaRampa()

    '''
        autor: isaacmsl
        nota:

        e a publicação com delay?
    '''
    def emFrente(): ''' seguir linha '''
        self.dataMotores = [self.VEL_ESQ_FRENTE, self.VEL_DIR_FRENTE]
        self.pubMotores(self.dataMotores)
    def direita():
        self.dataMotores = [self.VEL_ESQ_FRENTE, self.VEL_DIR_TRAS]
        self.pubMotores(self.dataMotores)
    def esquerda():
        self.dataMotores = [self.VEL_ESQ_TRAS, self.VEL_DIR_FRENTE]
        self.pubMotores(self.dataMotores)
    def paraTras():
        self.dataMotores = [self.VEL_ESQ_TRAS, self.VEL_DIR_TRAS]
        self.pubMotores(self.dataMotores)
    def parar():
        self.dataMotores = [0, 0]
        self.pubMotores(self.dataMotores)

    def emFrenteRampa(): ''' subir rampa '''
        self.dataMotores = [self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_FRENTE_RAMPA]
        self.pubMotores(self.dataMotores)
    def direitaRampa():
        self.dataMotores = [self.VEL_ESQ_FRENTE_RAMPA, self.VEL_DIR_TRAS_RAMPA]
        self.pubMotores(self.dataMotores)
    def esquerdaRampa():
        self.dataMotores = [self.VEL_ESQ_TRAS_RAMPA, self.VEL_DIR_FRENTE_RAMPA]
        self.pubMotores(self.dataMotores)
