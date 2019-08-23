#!/usr/bin/env python

import rospy
import cmdGarras
from byakugan.msg import SensoresDistanciaMsg, BoolGarras
from std_msgs.msg import Int32MultiArray

class PegarBola:
    def callback(self, data):
        distancia =  data.sensoresDistancia[0]
        if(distancia > 25):
            rospy.loginfo(" Estou longe")
            self.acionarMotores(30, 30)
        elif not self.pegueiVitima:
            rospy.loginfo("Estou perto")
            self.acionarMotores(0,0)
            self.cmd.abaixarBraco()
            self.cmd.abrirMao()
            self.cmd.fecharMao()
            self.cmd.subirBraco()
            self.pegueiVitima = True

    def acionarMotores(self, esq, dir):
        self.dataMotores.data = [esq, dir]
        self.moveMotores.publish(self.dataMotores)

    def __init__(self):
        rospy.init_node("pegarVitima")
        self.pegueiVitima = False
        self.dataMotores = Int32MultiArray()

        self.dataMotores.data = [0,0]
        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmd = cmdGarras.CmdGarras(self.pubGarras)
        rospy.Subscriber('distancia', SensoresDistanciaMsg, self.callback)
        self.moveMotores = rospy.Publisher('ctrl_motores', Int32MultiArray , queue_size=10, latch=True)
        rospy.spin()


if __name__ == "__main__":
    pegaBola = PegarBola()
