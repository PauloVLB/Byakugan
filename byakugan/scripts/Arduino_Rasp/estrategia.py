#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolGarras, CtrlMotores

class Estrategia():
    def __init__(self):

        # publishers
        self.pubMotores = rospy.Publisher('est_motores', CtrlMotores, queue_size=10)
        self.pubGarras = rospy.Publisher('est_garras', BoolGarras, queue_size=10)

        self.posicaoRobo = 1 # 1 == SALA 1 E 2 // 2 == RAMPA // 3 == SALA

    def callbackEstrategia(self, refle, dist):

        rate = rospy.Rate(20)

        # setando
        refleMaisEsq = refle.refletancia[0]
        refleEsq = refle.refletancia[1]
        refleDir = refle.refletancia[2]
        refleMaisDir = refle.refletancia[3]

        # falta testar sonares?
        sonarFrontal = dist.sensoresDistancia[0]
        sonarDir = dist.sensoresDistancia[1]
        sonarEsq = dist.sensoresDistancia[2]

        # sala 1 e 2
        if self.posicaoRobo == 1:
           # seguir linha
           if esq > 4 and dir > 4: # branco, branco
               self.roboEmFrente()
           elif esq > 4 and dir < 4: # branco, preto
               self.roboDir()
           elif esq < 4 and dir > 4: # preto, branco
               self.roboEsq()
           elif esq < 4 and dir < 4: # preto, preto
               self.roboParaTras()
        '''
        elif self.posicaoRobo == 2:
            # subir rampa
            if esq > 4 and dir > 4: # branco, branco
                emFrenteRampa()
            elif esq > 4 and dir < 4: # branco, preto
                direitaRampa()
            elif esq < 4 and dir > 4: # preto, branco
                esquerdaRampa()
            elif esq < 4 and dir < 4: # preto, preto
                emFrenteRampa()
                #self.posicao = 3
        elif self.posicaoRobo == 3:
            #sala 3
        '''

    def roboEmFrente(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboEsq(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboDir(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboParaTras(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboParar(self, delay=0):
        dataMotores = CtrlMotores()
        self.pubMotores.publish(dataMotores)




    def roboEmFrenteRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboEsqRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
    def roboDirRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)

    # pubs garras
    def abaixarBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 1
        self.pubGarras.publish(dataGarras)
    def subirBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 2
        self.pubGarras.publish(dataGarras)
    def abrirMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 2
        self.pubGarras.publish(dataGarras)
    def fecharMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 1
        self.pubGarras.publish(dataGarras)

    def loop(self):
        '''
        subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
        subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

        ts = message_filters.TimeSynchronizer([subRefle, subDistancia], 10)
        ts.registerCallback(self.callbackEstrategia)

        rospy.spin()
        '''
if __name__ == "__main__":
    rospy.init_node('estrategia', anonymous=False)
    estrategia = Estrategia()
    estrategia.loop()
