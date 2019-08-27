#!/usr/bin/env python

import rospy
import os
import cmdGarras
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import SensoresDistanciaMsg, BoolGarras, CtrlMotores
from std_msgs.msg import Int32MultiArray
import cmdMotores
import time

class PegarBola:
    def callback(self, init, coordenadas):
        if init.data:
            if self.executou == False:
                x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z

                if( r < 48 and self.encontrei == False ):
                    self.cmd.abrirMao()
                    self.cmd.abaixarBraco()

                    rospy.loginfo("Estou longe")
                    self.cmdMotores.roboAcionarMotores(30, 34)
                else:
                    self.cmdMotores.roboParar(.8)
                    rospy.loginfo("Estou perto")
                    self.encontrei = True

                    self.cmd.fecharMao()
                    self.cmd.subirBraco()

                    self.initResgatar()
            else:
                print 'estou true'

    def initResgatar(self):
        initData = Bool()
        initData.data = True
        self.pubResgatar.publish(initData)
        self.executou = True

    def acionarMotores(self, esq, dir):
        self.dataMotores.data = [esq, dir]
        self.moveMotores.publish(self.dataMotores)

    def __init__(self):
        rospy.init_node("pegarVitima")
        rospy.on_shutdown(self.resgatar)
        self.encontrei = False
        self.dataMotores = Int32MultiArray()
        self.dataMotores.data = [0,0]
        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmd = cmdGarras.CmdGarras(self.pubGarras)
        rospy.Subscriber('coordenadas_circulos', Vector3Stamped, self.callback)

        self.moveMotores = rospy.Publisher('cmdMotores', CtrlMotores , queue_size=10, latch=True)
        self.cmdMotores = cmdMotores.CmdMotores(self.moveMotores)
        self.executou = False

        subInit = message_filters.Subscriber('initPegar', Bool)
        subMotores = message_filters.Subscriber('cmdMotores', CtrlMotores)

        ts = message_filters.TimeSynchronizer([subInti, subMotores], 20)
        ts.registerCallback(self.callback)


if __name__ == "__main__":
    pegaBola = PegarBola()
    rospy.spin()
