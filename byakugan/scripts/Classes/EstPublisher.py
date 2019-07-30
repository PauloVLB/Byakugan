#!/usr/bin/env python

import rospy
from byakugan.msg import BoolGarras, CtrlMotores
class EstPublisher():
    def __init__(self):

        self.rate = rospy.Rate(230)

        self.pubMotores = rospy.Publisher('est_motores', CtrlMotores, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on est_motores [byakugan/CtrlMotores]")

        self.pubGarras = rospy.Publisher('est_garras', BoolGarras, queue_size=10, latch=True)
        rospy.loginfo("Setup publisher on est_garras [byakugan/BoolGarras]")

    def roboAcionarMotores(self, esq, dir, delay=0):
        if esq < 100 and dir < 100:
            dataMotores = CtrlMotores()
            dataMotores.esq.data = esq
            dataMotores.dir.data = dir
            dataMotores.delay.data = delay
            self.pubMotores.publish(dataMotores)
            rospy.loginfo("[PUBLISHED] roboAcionarMotores!")
            self.rate.sleep()

    def roboEmFrente(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEmFrente!")
        self.rate.sleep()
    def roboEsq(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEsq!")
        self.rate.sleep()
    def roboDir(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        print 'passei'
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboDir!")
        self.rate.sleep()
    def roboParaTras(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.esq.data = -1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboParaTras!")
        self.rate.sleep()
    def roboParar(self, delay=0):
        dataMotores = CtrlMotores()
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboParar!")
        self.rate.sleep()




    def roboEmFrenteRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEmFrenteRampa!")
        self.rate.sleep()
    def roboEsqRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = -1
        dataMotores.dir.data = 1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboEsqRampa!")
        self.rate.sleep()
    def roboDirRampa(self, delay=0):
        dataMotores = CtrlMotores()
        dataMotores.rampa.data = True
        dataMotores.esq.data = 1
        dataMotores.dir.data = -1
        dataMotores.delay.data = delay
        self.pubMotores.publish(dataMotores)
        rospy.loginfo("[PUBLISHED] roboDirRampa!")
        self.rate.sleep()

    # pubs garras
    def abaixarBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 1
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] abaixarBraco!")
        self.rate.sleep()
    def subirBraco(self):
        dataGarras = BoolGarras()
        dataGarras.braco.data = 2
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] subirBraco!")
        self.rate.sleep()
        print 'published'
    def abrirMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 2
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] abrirMao!")
        self.rate.sleep()
    def fecharMao(self):
        dataGarras = BoolGarras()
        dataGarras.mao.data = 1
        self.pubGarras.publish(dataGarras)
        rospy.loginfo("[PUBLISHED] fecharMao!")
        self.rate.sleep()
