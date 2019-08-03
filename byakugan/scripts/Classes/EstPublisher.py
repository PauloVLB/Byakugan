#!/usr/bin/env python

import rospy
from byakugan.msg import BoolGarras, CtrlMotores
class EstPublisher():
    def __init__(self):

        self.rate = rospy.Rate(230)

        self.dataMotores = CtrlMotores()
        self.dataGarras = BoolGarras()

        self.pubMotores = rospy.Publisher('est_motores', CtrlMotores, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on est_motores [byakugan/CtrlMotores]")

        self.pubGarras = rospy.Publisher('est_garras', BoolGarras, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on est_garras [byakugan/BoolGarras]")

    def setDataMotores(self, esq, dir, delay, rampa=False):
        self.dataMotores.esq.data = esq
        self.dataMotores.dir.data = dir
        self.dataMotores.rampa.data = rampa
        self.dataMotores.delay.data = delay
        
    def setDataGarras(self, mao, braco):
        self.dataGarras.mao.data = mao
        self.dataGarras.braco.data = braco

    def roboAcionarMotores(self, esq, dir, delay=0):
        if esq < 100 and dir < 100:
            self.setDataMotores(esq, dir, delay)
            self.pubMotores.publish(dataMotores)
            #rospy.loginfo("[PUBLISHED] roboAcionarMotores!")
            self.rate.sleep()

    def roboEmFrente(self, delay=0):
        self.setDataMotores(1, 1, delay)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboEmFrente!")
        self.rate.sleep()

    def roboEsq(self, delay=0):
        self.setDataMotores(-1, 1, delay)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboEsq!")
        self.rate.sleep()
    
    def roboDir(self, delay=0):
        self.setDataMotores(1, -1, delay)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboDir!")
        self.rate.sleep()

    def roboParaTras(self, delay=0):
        self.setDataMotores(-1, -1, delay)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboParaTras!")
        self.rate.sleep()

    def roboParar(self, delay=0):
        self.setDataMotores(0, 0, delay)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboParar!")
        self.rate.sleep()




    def roboEmFrenteRampa(self, delay=0):
        rampa = True
        self.setDataMotores(1, 1, delay, rampa)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboEmFrenteRampa!")
        self.rate.sleep()

    def roboEsqRampa(self, delay=0):
        rampa = True
        self.setDataMotores(-1, 1, delay, rampa)
        #rospy.loginfo("[PUBLISHED] roboEsqRampa!")
        self.rate.sleep()

    def roboDirRampa(self, delay=0):
        rampa = True
        self.setDataMotores(1, -1, delay, rampa)
        self.pubMotores.publish(dataMotores)
        #rospy.loginfo("[PUBLISHED] roboDirRampa!")
        self.rate.sleep()

    # pubs garras
    def abaixarBraco(self):
        mao = 0
        braco = 1
        self.setDataGarras(mao, braco)
        self.pubGarras.publish(dataGarras)
        #rospy.loginfo("[PUBLISHED] abaixarBraco!")
        self.rate.sleep()

    def subirBraco(self):
        mao = 0
        braco = 2
        self.setDataGarras(mao, braco)
        self.pubGarras.publish(dataGarras)
        #rospy.loginfo("[PUBLISHED] subirBraco!")
        self.rate.sleep()
    
    def abrirMao(self):
        mao = 2
        braco = 0
        self.setDataGarras(mao, braco)
        self.pubGarras.publish(dataGarras)
        #rospy.loginfo("[PUBLISHED] abrirMao!")
        self.rate.sleep()
    
    def fecharMao(self):
        mao = 1
        braco = 0
        self.setDataGarras(mao, braco)
        self.pubGarras.publish(dataGarras)
        #rospy.loginfo("[PUBLISHED] fecharMao!")
        self.rate.sleep()
