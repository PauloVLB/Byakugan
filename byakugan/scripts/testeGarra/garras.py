#!/usr/bin/env python
# -*- conding: utf-8 -*-

import rospy
import time
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolGarras

class Garras():
    def __init__(self):

        rospy.init_node('garras', anonymous=False)

        # braco
        self.ANG_INICIAL_BAIXAR_BRACO = 80
        self.ANG_FINAL_BAIXAR_BRACO = 10

        self.ANG_INICIAL_SUBIR_BRACO = 10
        self.ANG_FINAL_SUBIR_BRACO = 80

        # mao
        self.ANG_INICIAL_ABRIR_MAO = 90
        self.ANG_FINAL_ABRIR_MAO = 0

        self.ANG_INICIAL_FECHAR_MAO = 0
		self.ANG_FINAL_FECHAR_MAO = 90

        self.DELAY = 0.2
        self.BRACO = 1
        self.MAO = 2

        self.angAtualMao = 90
        self.angAtualBraco = 90

        # publisher
        self.pubGarras = rospy.Publisher('ctrl_garras', Int32MultiArray, queue_size=10)

        self.listener() ''' inicia o loop '''

    def listener():
        rospy.Subscriber('est_garras', BoolGarras, callback)
        rospy.spin()
    def callback(dataGarras):
        # mao - True: abrir False: fechar
        # braco - True: subir False: abaixar

        if dataGarras.mao: ''' falta testar '''
            self.abrirMao()
        else:
            self.fecharMao()

        if dataGarras.braco:
            self.abrirBraco()
        else:
            self.abaixarBraco()

    def setPosicao(servo ,angInicial, angFinal, delay=self.DELAY):
        dataGarras = Int32MultiArray()
        if angInicial > angFinal:
            for i in range(angInicial, angFinal):
                if servo == self.BRACO:
                    dataGarras.data [i, self.angAtualMao] # [braco, mao]
                    self.angAtualBraco = i
                elif self.MAO:
                    dataGarras.data [self.angAtualBraco, i] # [braco, mao
                    self.angAtualMao = i
                pubGarras.publish(dataGarras)
                if not i == angFinal:
                    time.sleep(delay)
        else:
            for i in range(angInicial, angFinal, -1):
                if servo == self.BRACO:
                    dataGarras.data [i, self.angAtualMao] # [braco, mao]
                    self.angAtualBraco = i
                elif self.MAO:
                    dataGarras.data [self.angAtualBraco, i] # [braco, mao
                    self.angAtualMao = i
                pubGarras.publish(dataGarras)
                if not i == angFinal:
                    time.sleep(delay)

    def abaixarBraco():
        self.setPosicao(self.BRACO, self.ANG_INICIAL_BAIXAR_BRACO, self.ANG_FINAL_BAIXAR_BRACO)
    def subirBraco():
        self.setPosicao(self.BRACO, self.ANG_INICIAL_SUBIR_BRACO, self.ANG_FINAL_SUBIR_BRACO)
    def abrirMao():
        self.setPosicao(self.MAO, self.ANG_INICIAL_ABRIR_MAO, self.ANG_FINAL_FECHAR_MAO)
    def fecharMao():
        self.setPosicao(self.MAO, self.ANG_INICIAL_FECHAR_MAO, self.ANG_FINAL_FECHAR_MAO)
