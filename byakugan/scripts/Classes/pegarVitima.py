#!/usr/bin/env python

import rospy
from byakugan.msg import SensoresDistanciaMsg
from std_msgs.msg import Int32MultiArray 

class PegarBola:  
    def callback(self, data):   
        distancia =  data.sensoresDistancia[0]
        if(distancia > 15):
            rospy.loginfo("longe")
            self.acionarMotores(25, 25)
        else:
            rospy.loginfo("perto")
            self.acionarMotores(0,0)
            
             
    def acionarMotores(self, esq, dir):
        self.dataMotores.data = [esq, dir]
        self.moveMotores.publish(self.dataMotores)


    def __init__(self):   
        #print "entrei aqui" 
        rospy.init_node("PegarBola")
        self.dataMotores = Int32MultiArray()
        self.dataMotores.data = [0,0]       
        rospy.Subscriber("distancia", SensoresDistanciaMsg, self.callback)
        self.moveMotores = rospy.Publisher("ctrl_motores", Int32MultiArray , queue_size=10, latch=True) 
        rospy.spin()    


if __name__ == "__main__":
    pegaBola = PegarBola()
    