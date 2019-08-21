#!/usr/bin/env python

import FindRectangle

import rospy
import message_filters
from std_msgs.msg import Empty

class Resgate():
    def __init__(self):
        rospy.init_node("resgate", anonymous=False)

        #self.motores = Motores()
        self.motores = Int32MultiArray()
        self.pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)

        subInit = message_filters.Subscriber('init_resgate', Empty)
        subRectangle = message_filters.Subscriber('centroid_rectangle', CentroidObject)

        ts = message_filters.TimeSynchronizer([subInit, subRectangle], 20)

        ts.registerCallback(self.callback)

    def acionarMotores(self, esq, dir):
        self.motores.data = [esq, dir]
        rospy.loginfo(self.motores.data)
        self.pubMotores.publish(self.motores)

    def callback(self, init,centroid):

        '''
        if init == {}: # testar
            # iniciar procura da area
            pass
        '''

        diferenca = centroid.diferenca.data
        if diferenca < 0: # area na esq
            #self.motores.roboAcionarMotores(-35, 35)
            self.acionarMotores(-25, 25)
            pass
        elif diferenca == 0:
            # se alinhou!!!!
            self.acionarMotores(0, 0)
            pass
        elif diferenca > 0: # area na dir
            #self.motores.roboAcionarMotores(35, -35)
            self.acionarMotores(25, -25)
            pass


if __name__ == "__main__":
    node = Resgate()
    rospy.spin()
