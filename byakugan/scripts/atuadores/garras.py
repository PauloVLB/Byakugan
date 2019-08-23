#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolGarras

class Garras():
    def __init__(self):
        rospy.Subscriber('cmdGarras', BoolGarras, self.__callback)

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

        self.DELAY = 0.005
        self.BRACO = 1 # diferenciando a publicacao para o braco e a mao
        self.MAO = 2 # diferenciando a publicacao para o braco e a mao

        self.cacheBraco = 2 # levantado
        self.cacheMao = 1 # fechada

        self.angAtualMao = 90
        self.angAtualBraco = 90

        # publisher
        self.rate = rospy.Rate(20)
        self.pubGarras = rospy.Publisher('ctrl_garras', Int32MultiArray, queue_size=10)
        rospy.loginfo("Setup publisher on ctrl_motores [std_msgs.msg/Int32MultiArray]")

    def __callback(self, dataGarras):
        # mao - 2: abrir 1: fechar 0: nada
        # braco - 2: subir 1: abaixar 0: nada

        rospy.loginfo(rospy.get_caller_id() + " - msg received!")

        # testar

        dataMao = dataGarras.mao.data
        dataBraco = dataGarras.braco.data

        if dataMao == 2 and dataMao != self.cacheMao: # impede publicações desnecessárias
            self.__abrirMao()
            self.cacheMao = dataMao
            rospy.loginfo("Note: cacheMao was changed to " + str(dataMao))
        elif dataMao == 1 and dataMao != self.cacheMao:
            self.__fecharMao()
            self.cacheMao = dataMao
            rospy.loginfo("Note: cacheMao was changed to " + str(dataMao))

        if dataBraco == 2 and dataBraco != self.cacheBraco:
            self.__subirBraco()
            self.cacheBraco = dataBraco
            rospy.loginfo("Note: cacheBraco was changed to " + str(dataBraco))
        elif dataBraco == 1 and dataBraco != self.cacheBraco:
            self.__abaixarBraco()
            self.cacheBraco = dataBraco
            rospy.loginfo("Note: cacheBraco was changed to " + str(dataBraco))

    def __setPosicao(self, servo, angInicial, angFinal, delay=None):
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
                rospy.loginfo("[PUBLISHED] ctrl_garras -> " + str(dataGarras.data))
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
                rospy.loginfo("[PUBLISHED] ctrl_garras -> " + str(dataGarras.data))
                #print dataGarras
                if not i == angFinal:
                    time.sleep(float(delay))

    def __abaixarBraco(self):
        self.__setPosicao(self.BRACO, self.ANG_INICIAL_BAIXAR_BRACO, self.ANG_FINAL_BAIXAR_BRACO)
    def __subirBraco(self):
        self.__setPosicao(self.BRACO, self.ANG_INICIAL_SUBIR_BRACO, self.ANG_FINAL_SUBIR_BRACO)
    def __abrirMao(self):
        self.__setPosicao(self.MAO, self.ANG_INICIAL_ABRIR_MAO, self.ANG_FINAL_ABRIR_MAO)
    def __fecharMao(self):
        self.__setPosicao(self.MAO, self.ANG_INICIAL_FECHAR_MAO, self.ANG_FINAL_FECHAR_MAO)

if __name__ == "__main__":
    rospy.init_node('garras', anonymous=False)
    garras = Garras()
    rospy.spin()
