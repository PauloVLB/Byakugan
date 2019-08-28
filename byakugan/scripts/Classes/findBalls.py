#!/usr/bin/env python
import rospy
import numpy
import os
import message_filters
import cmdMotores
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Int32MultiArray
from byakugan.msg import BoolStamped, SensoresDistanciaMsg, BotoesMsg, CtrlMotores

class FindBalls:
    def __init__(self):
        rospy.init_node("findBalls", anonymous=False)

        self.achouVitima = False
        self.executou = False

        self.pubMotores = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10)
        self.pubPegar = rospy.Publisher("initPegar", BoolStamped, queue_size=10, latch=True)

        self.cmd = cmdMotores.CmdMotores(self.pubMotores)
        subCoordinates = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)
        subBall = message_filters.Subscriber('tem_circulos', BoolStamped)

        ts = message_filters.TimeSynchronizer([subCoordinates, subBall], 20)
        ts.registerCallback(self.ballsCb)

    def initPegar(self):
        initData = BoolStamped()
        initData.existe.data = True
        self.pubPegar.publish(initData)
        self.executou = True

    def ballsCb(self, coordinates, circle):

        if self.executou == False:
            x, y, r = coordinates.vector.x, coordinates.vector.y, coordinates.vector.z

            if circle.existe.data:
                self.achouVitima = True
                if self.achouVitima:
                    self.cmd.roboDir(.07)
                    self.cmd.roboAcionarMotores(0, 0)

                    self.initPegar()

                    '''
                    if x in numpy.arange(200, 280, 1):
                        self.cmd.roboAcionarMotores(0, 0)
                        self.pegarVitima()
                    '''
            else:
                self.cmd.roboAcionarMotores(25, -25)
        else:
            self.initPegar()
            rospy.loginfo('ja executei')

if __name__ == "__main__":
    node = FindBalls()
    rospy.spin()
