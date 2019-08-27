#!/usr/bin/env python

import rospy
import os
import cmdGarras
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import SensoresDistanciaMsg, BoolGarras
from std_msgs.msg import Int32MultiArray

class PegarBola:
    def callback(self, coordenadas):
        x, y, r = coordenadas.vector.x, coordenadas.vector.y, coordenadas.vector.z
        rospy.loginfo(r)
        if( r < 50 and self.encontrei == False ):
            rospy.loginfo("Estou longe")
            self.acionarMotores(30, 34)
        else:
            rospy.loginfo("Estou perto")
            self.acionarMotores(0,0)
            self.encontrei = True
            self.acionarGarras() 
            

    def acionarGarras(self):
        self.cmd.abrirMao()
        self.cmd.abaixarBraco()
        self.cmd.fecharMao()
        self.cmd.subirBraco()
        os.system("roslaunch byakugan resgatar.launch")
        

    def acionarMotores(self, esq, dir):
        self.dataMotores.data = [esq, dir]
        self.moveMotores.publish(self.dataMotores)

    def __init__(self):
        rospy.init_node("pegarVitima")
        self.encontrei = False
        self.dataMotores = Int32MultiArray()
        self.dataMotores.data = [0,0]
        self.pubGarras = rospy.Publisher('cmdGarras', BoolGarras, queue_size=10)
        self.cmd = cmdGarras.CmdGarras(self.pubGarras)
        rospy.Subscriber('coordenadas_circulos', Vector3Stamped, self.callback)
        
        self.moveMotores = rospy.Publisher('ctrl_motores', Int32MultiArray , queue_size=10, latch=True)
        


if __name__ == "__main__":
    pegaBola = PegarBola()
    rospy.spin()