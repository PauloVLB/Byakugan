#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolGarras

class Estrategia():
    def __init__(self):

        # publishers
        # est_motores -> Int32MultiArray?
        self.pubMotores = rospy.Publisher('est_motores', Int32MultiArray, queue_size=10)
        self.pubGarras = rospy.Publisher('est_garras', BoolGarras, queue_size=10)

        self.posicaoRobo = 1 # 1 == SALA 1 E 2 // 2 == RAMPA // 3 == SALA

        # garra
        self.garras = Garras()
        self.dataGarras = BoolGarras()

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

        # datas
        dataMotores = Int32MultiArray()
        dataGarras = Int32MultiArray()

        if self.posicaoRobo == 1: ''' sala 1 e 2 '''
           # seguir linha
           if(esq > 4 and dir > 4 ): # branco, branco
               dataMotores.data = [25, 25]
           elif (esq > 4 and dir < 4  ): # branco, preto
               dataMotores.data = [25, -25]
           elif (esq < 4 and dir > 4 ): # preto, branco
               dataMotores.data = [-25,25]
           elif (esq < 4 and dir < 4 ): # preto, preto
               dataMotores.data = [25, 25]

        elif self.posicaoRobo == 2: ''' rampa '''
            # subir rampa
            if(esq > 4 and dir > 4): # branco, branco
                dataMotores.data = [25, 25] # ?
            elif (esq > 4 and dir < 4  ): # branco, preto
                dataMotores.data = [25, -25] # ?
            elif (esq < 4 and dir > 4 ): # preto, branco
                dataMotores.data = [-25,25] # ?
            elif (esq < 4 and dir < 4 ): # preto, preto
                dataMotores.data = [25, 25] # ?
                #self.posicao = 3

        elif self.posicao == 3: ''' sala 3 '''

            # girar para alinhar
            dataMotores.data = [25, -25]
            #pubMotoresDelay(100)
            # encostar na parede
            dataMotores.data = [-25, -25]
            #pubMotoresDelay(200)
            # ir para frente
            dataMotores.data = [25, 25]
            #pubMotoresDelay(200)
            # encostar na parede
            dataMotores.data = [-25, -25]
            #pubMotoresDelay(200)

            ''' TESTE GARRA '''
            abaixarMao()

    def abaixarBraco():
        self.dataGarras.braco = False
        self.pubGarras.publish(self.dataGarras)
    def subirBraco():
        self.dataGarras.braco = True
        self.pubGarras.publish(self.dataGarras)
    def abrirMao():
        self.dataGarras.braco = True
        self.pubGarras.publish(self.dataGarras)
    def fecharMao():
        self.dataGarras.braco = False
        self.pubGarras.publish(self.dataGarras)

    def loop():
        rospy.init_node('estrategia', anonymous=True)
        subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
        subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

        ts = message_filters.TimeSynchronizer([subRefle, subDistancia], 10)
        ts.registerCallback(callbackEstrategia)

        rospy.spin()

if __name__ == "__main__":
	try:
        estrategia = Estrategia()
        estrategia.loop()
	except rospy.ROSInterruptException:
		pass
