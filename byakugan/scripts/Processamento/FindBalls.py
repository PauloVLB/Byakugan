#!/usr/bin/env python
import rospy 
import numpy
import message_filters
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, LedMsg

class FindBalls:
    def __init__(self):
        rospy.init_node("FindBalls", anonymous=True)

        self.motores = Int32MultiArray()
        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        
        self.leds = LedMsg()
        self.pubLeds = rospy.Publisher("ctrl_leds", LedMsg, queue_size=10)
        
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
        else:
            self.acionarMotores(25, -25)

    def acionarMotores(self, esq, dir):
        self.motores.data = [esq, dir]
        rospy.loginfo(self.motores.data)
        self.pubMotores.publish(self.motores)

    def setEstadoLed(self, led, estado):
        if led == 1:
            self.leds.led1.data = estado
        if led == 2:
            self.leds.led2.data = estado
        if led == 3:
            self.leds.led3.data = estado
        
        pubLeds.publish(self.leds)

if __name__ == "__main__":
    node = FindBalls()
    rospy.spin()