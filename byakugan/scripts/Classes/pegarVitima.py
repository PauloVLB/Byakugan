#!/usr/bin/env python


import rospy
import sys
sys.path.append("../atuadores")
import garras
from byakugan.msg import SensoresDistanciaMsg
from std_msgs.msg import Int32MultiArray 

class PegarBola:  
    def callback(self, data):   
        distancia =  data.sensoresDistancia[0]
        if(distancia > 15):
            rospy.loginfo(" Estou longe")
            self.acionarMotores(30, 30)
        else:
            rospy.loginfo("Estou perto")
            self.acionarMotores(0,0)
            #self.usaGarra()
            
                        
    def acionarMotores(self, esq, dir):
        self.dataMotores.data = [esq, dir]
        self.moveMotores.publish(self.dataMotores)

    #def usarGarra(self):
        #rospy.loginfo("Estou abaixando o braço")
        #self.dataGarras.abaixarBraco()
    
    def __init__(self):   
        rospy.init_node("pegarVitima")
        self.dataGarras = Garras()
        self.dataMotores = Int32MultiArray()
        self.dataMotores.data = [0,0]
        self.pubGarras = rospy.Publisher('cmdGarras', std_msgs/Int8, queue_size=10)       
        rospy.Subscriber('distancia', SensoresDistanciaMsg, self.callback)
        self.moveMotores = rospy.Publisher('ctrl_motores', Int32MultiArray , queue_size=10, latch=True) 
        rospy.spin()    


if __name__ == "__main__":
    pegaBola = PegarBola()
    