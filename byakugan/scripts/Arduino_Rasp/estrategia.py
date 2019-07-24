#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolGarras, CtrlMotores

class Estrategia():
    def __init__(self):

        # publishers

        self.pubMotores = rospy.Publisher('est_motores', CtrlMotores, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on est_motores [byakugan/CtrlMotores]")
        '''
        self.pubGarras = rospy.Publisher('est_garras', BoolGarras, queue_size=10)
        dataGarras = BoolGarras()
        self.pubGarras.publish(dataGarras) # estabelece comunicação inicial
        '''
        self.posicaoRobo = 1 # 1 == SALA 1 E 2 // 2 == RAMPA // 3 == SALA

        #def callback(self, refle, dist):
    def callback(self, refle):

        rospy.loginfo(rospy.get_caller_id() + " - msg received!")

        #rate = rospy.Rate(20)

        # setando
        refleMaisEsq = refle.refletancia[0]
        refleEsq = refle.refletancia[1]
        refleDir = refle.refletancia[2]
        refleMaisDir = refle.refletancia[3]

        '''
        sonarFrontal = dist.sensoresDistancia[0]
        sonarDir = dist.sensoresDistancia[1]
        sonarEsq = dist.sensoresDistancia[2]
        '''

        # sala 1 e 2
        if self.posicaoRobo == 1:
           # seguir linha
           if refleEsq >= 4 and refleDir >= 4: # branco, branco
               self.roboEmFrente()
           elif refleEsq >= 4 and refleDir < 4: # branco, preto
               self.roboDir()
           elif refleEsq < 4 and refleDir >= 4: # preto, branco
               self.roboEsq()
           elif refleEsq < 4 and refleDir < 4: # preto, preto
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

    def roboAcionarMotores(self, esq, dir, delay=0):
        if esq < 100 and dir < 100:
            dataMotores = CtrlMotores()
            dataMotores.esq.data = esq
            dataMotores.dir.data = dir
            dataMotores.delay.data = delay
            self.pubMotores.publish(dataMotores)
            rospy.loginfo("[PUBLISHED] roboAcionarMotores!")

    def roboEmFrente(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEmFrente!")
    def roboEsq(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEsq!")
    def roboDir(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        print 'passei'
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboDir!")
    def roboParaTras(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboParaTras!")
    def roboParar(self, delay=0):
        dataMotores = CtrlMotores()
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboParar!")




    def roboEmFrenteRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEmFrenteRampa!")
    def roboEsqRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEsqRampa!")
    def roboDirRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboDirRampa!")

    # pubs garras
    def abaixarBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 1
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] abaixarBraco!")
    def subirBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 2
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] subirBraco!")
        print 'published'
    def abrirMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 2
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] abrirMao!")
    def fecharMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 1
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] fecharMao!")

    def loop(self):
        '''
        subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
        subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

        ts = message_filters.TimeSynchronizer([subRefle, subDistancia], 10)
        ts.registerCallback(self.callbackEstrategia)
        '''

        rospy.Subscriber('refletancia', RefletanciaMsg, self.callback)
        rospy.loginfo("Setup subscriber on refletancia [RefletanciaMsg]")

        rospy.spin()

if __name__ == "__main__":
    rospy.init_node('estrategia', anonymous=False)
    estrategia = Estrategia()
    estrategia.loop()
