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

        # motores
        self.dataMotores = CtrlMotores() # msg

        # garras
        self.garras = Garras() # class
        self.dataGarras = BoolGarras() # msg

    def callbackEstrategia(refle, dist):

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


        if self.posicaoRobo == 1: ''' sala 1 e 2 '''
           # seguir linha
           if(esq > 4 and dir > 4 ): # branco, branco
               emFrente()
           elif (esq > 4 and dir < 4  ): # branco, preto
               direita()
           elif (esq < 4 and dir > 4 ): # preto, branco
               esquerda()
           elif (esq < 4 and dir < 4 ): # preto, preto
               paraTras()

        elif self.posicaoRobo == 2: ''' rampa '''
            # subir rampa
            if(esq > 4 and dir > 4): # branco, branco
                emFrenteRampa()
            elif (esq > 4 and dir < 4  ): # branco, preto
                direitaRampa()
            elif (esq < 4 and dir > 4 ): # preto, branco
                esquerdaRampa()
            elif (esq < 4 and dir < 4 ): # preto, preto
                emFrenteRampa()
                #self.posicao = 3

        elif self.posicao == 3: ''' sala 3 '''

            # girar para alinhar
            direita()
            #pubMotoresDelay(100)
            # encostar na parede
            paraTras()
            #pubMotoresDelay(200)
            # ir para frente
            emFrente() ''' !!!!!!!!!!!! NÃO QUERO VELOCIDADE PADRÃO, E AGORA?'''
            #pubMotoresDelay(200)
            # encostar na parede
            dataMotores.data = [-25, -25]
            #pubMotoresDelay(200)

            ''' TESTE GARRA '''
            abaixarMao()

    def emFrente(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq = 1
        dataMotores.dir = 1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def esquerda(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq = -1
        dataMotores.dir = 1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def direita(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq = 1
        dataMotores.dir = -1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def paraTras(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq = -1
        dataMotores.dir = -1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def parar(delay=0):
        dataMotores = CtrlMotores()
        self.pubMotores.publish(dataMotores)

    def emFrenteRampa(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa = True
        dataMotores.esq = 1
        dataMotores.dir = 1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def esquerdaRampa(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa = True
        dataMotores.esq = 1
        dataMotores.dir = -1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)
    def direitaRampa(delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa = True
        dataMotores.esq = -1
        dataMotores.dir = 1
        dataMotores.delay = delay
        self.pubMotores.publish(dataMotores)

    # pubs garras
    def abaixarBraco():
        self.dataGarras.braco = False
        self.pubGarras.publish(self.dataGarras)
    def subirBraco():
        self.dataGarras.braco = True
        self.pubGarras.publish(self.dataGarras)
    def abrirMao():
        self.dataGarras.mao = True
        self.pubGarras.publish(self.dataGarras)
    def fecharMao():
        self.dataGarras.mao = False
        self.pubGarras.publish(self.dataGarras)

    def loop():
        rospy.init_node('estrategia', anonymous=True)
        subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
        subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

        ts = message_filters.TimeSynchronizer([subRefle, subDistancia], 10)
        ts.registerCallback(callbackEstrategia)

        rospy.spin()

if __name__ == "__main__":
	estrategia = Estrategia()
    estrategia.loop()
