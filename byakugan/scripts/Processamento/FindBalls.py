#!/usr/bin/env python
import rospy 
import numpy
import os
import message_filters
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg

class FindBalls:
    def __init__(self):
        rospy.init_node("FindBalls", anonymous=True)
    
        self.motores = Int32MultiArray()
        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        
        subBtns = message_filters.Subscriber('botoes', BotoesMsg)  
        subDist = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
        subCoordinates = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        subBall = message_filters.Subscriber('tem_circulos', BoolStamped)
        
        ts = message_filters.TimeSynchronizer([subCoordinates, subBall, subDist, subBtns], 20)
        
        ts.registerCallback(self.ballsCb)

    def ballsCb(self, coordinates, circle, dist, btns):
        x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

        if circle.existe.data:
            self.acionarMotores(0, 0)
            os.system("rosrun byakugan pegarVitima.py")
        else:
            self.acionarMotores(25, -25)

    def acionarMotores(self, esq, dir):
        self.motores.data = [esq, dir]
        rospy.loginfo(self.motores.data)
        self.pubMotores.publish(self.motores)

if __name__ == "__main__":
    node = FindBalls()
    rospy.spin()