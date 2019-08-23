#!/usr/bin/env python

import rospy
import cmdMotores
from std_msgs.msg import Int32MultiArray, Int16
from byakugan.msg import LedMsg, CtrlMotores, BoolStamped

import rospy
class Resgate():
    def __init__(self):
        rospy.init_node("resgate", anonymous=False)

        self.pub = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10, latch=True)
        self.cmd = cmdMotores.CmdMotores(self.pub)

        self.pubLeds = rospy.Publisher("ctrl_leds", LedMsg, queue_size=10, latch=True)
        self.dataLeds = LedMsg()

        rospy.Subscriber('centroid_rectangle', BoolStamped, self.callback)

    def acionarMotores(self, esq, dir):
        self.motores.data = [esq, dir]
        rospy.loginfo(self.motores.data)
        self.pubMotores.publish(self.motores)

    def publishLeds(self, led1, led2, led3):
        self.dataLeds.led1.data = led1
        self.dataLeds.led2.data = led2
        self.dataLeds.led3.data = led3
        self.pubLeds.publish(self.dataLeds)

    def callback(self, areaBool):

        if areaBool.existe.data == False:
            #self.publishLeds(0, 1, 0)
            rospy.loginfo("cade a tete?")
            self.cmd.roboAcionarMotores(25, -25)
        else:
            if areaBool.centroid.data > 20: # area na esq
                #self.publishLeds(1, 0, 0)
                rospy.loginfo("area na esq")
                self.cmd.roboAcionarMotores(-25, 25)
                #pass
            elif areaBool.centroid.data < -10: # area na dir
                #self.publishLeds(0, 0, 1)
                rospy.loginfo("area na dir")
                self.cmd.roboAcionarMotores(25, -25)
                #pass
            else:
                rospy.loginfo("achei a tete!!!")
                self.cmd.roboAcionarMotores(0, 0)




if __name__ == "__main__":
    node = Resgate()
    rospy.spin()
