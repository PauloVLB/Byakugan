#!/usr/bin/env python

import rospy
import SensoresListener
from byakugan.msg import SensoresDistanciaMsg, BotoesMsg, CtrlMotores
 
 
class PegarBola:
    
    def callback(self, data):
        indoBola = True
        while(chegouBola):
            distancia = sensorEscuta.getDist(0)
            if(distacia > 10):
                acionaMotores(45, 45)
            elif( distancia < 10):
                acionaMotores(0,0)
                indoBola = False
             
    def acionaMotores(esq, dir):
        motorMove.esq.data = esq
        motorMove.dir.data = dir
        moveMotores.publish(motorMove)


    def __init__(self):
        rospy.init_node("PegarBola")
        rospy.Subscriber("distacia",SensoresDistanciaMsg, callback)
        rospy.Subscriber("botoes",BotoesMsg,callback) 
        moveMotores = rospy.Publisher("ctrl_motores", CtrlMotores, queue_size=10) 
        motorMove = CtrlMotores()       
        sensorEscuta = SensoresListener()
        pass


if __name__ == "__main__":
    ros_node = RosNode()
    rospy.spin()