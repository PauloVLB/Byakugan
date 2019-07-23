#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolGarras

class Garras():
    def __init__(self):


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

        self.DELAY = 0.05
        self.BRACO = 1 # diferenciando a publicacao para o braco e a mao
        self.MAO = 2 # diferenciando a publicacao para o braco e a mao

        self.angAtualMao = 90
        self.angAtualBraco = 90

        # publisher
        self.rate = rospy.Rate(20)
        self.pubGarras = rospy.Publisher('ctrl_garras', Int32MultiArray, queue_size=10)

    def listener(self):
        rospy.Subscriber('est_garras', BoolGarras, self.callback)
        rospy.spin()
    def callback(self, dataGarras):
        # mao - True: abrir False: fechar
        # braco - True: subir False: abaixar

        print 'backei'

        # testar
        if dataGarras.mao.data == 2:
            self.abrirMao()
        elif not dataGarras.mao.data == 1:
            self.fecharMao()
        elif dataGarras.braco.data == 2:
            self.subirBraco()
        elif dataGarras.braco.data == 1:
            self.abaixarBraco()

    def setPosicao(self, servo, angInicial, angFinal, delay=None):
        if delay is None:
            delay = self.DELAY

        dataGarras = Int32MultiArray()
        if angInicial > angFinal: # diminuir angulo
            # publica em espaços aos poucos do angInicial ao angFinal
            for i in range(angInicial, angFinal, -1):
                if servo == self.BRACO: # diferenciando a publicacao para o braco e a mao
                    dataGarras.data = [i, self.angAtualMao] # [braco, mao]
                    self.angAtualBraco = i
                elif servo == self.MAO:
                    dataGarras.data = [self.angAtualBraco, i] # [braco, mao
                    self.angAtualMao = i

                self.pubGarras.publish(dataGarras)
                #print dataGarras
                if not i == angFinal:
                    time.sleep(float(delay))

        else:
            # publica em espaços aos poucos do angInicial ao angFinal
            for i in range(angInicial, angFinal):
                if servo == self.BRACO: # diferenciando a publicacao para o braco e a mao
                    dataGarras.data = [i, self.angAtualMao] # [braco, mao]
                    self.angAtualBraco = i
                elif servo == self.MAO:
                    dataGarras.data = [self.angAtualBraco, i] # [braco, mao
                    self.angAtualMao = i

                self.pubGarras.publish(dataGarras)
                #print dataGarras
                if not i == angFinal:
                    time.sleep(float(delay))

    def abaixarBraco(self):
        self.setPosicao(self.BRACO, self.ANG_INICIAL_BAIXAR_BRACO, self.ANG_FINAL_BAIXAR_BRACO)
    def subirBraco(self):
        self.setPosicao(self.BRACO, self.ANG_INICIAL_SUBIR_BRACO, self.ANG_FINAL_SUBIR_BRACO)
    def abrirMao(self):
        self.setPosicao(self.MAO, self.ANG_INICIAL_ABRIR_MAO, self.ANG_FINAL_ABRIR_MAO)
    def fecharMao(self):
        self.setPosicao(self.MAO, self.ANG_INICIAL_FECHAR_MAO, self.ANG_FINAL_FECHAR_MAO)

if __name__ == "__main__":
    rospy.init_node('garras', anonymous=False)
    garras = Garras()
    garras.listener()
