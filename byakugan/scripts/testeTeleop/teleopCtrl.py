#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from byakugan.msg import CtrlMotores
import cmdMotores

class TeleopCtrl():
    def __init__(self):
        self.running = 0
        rospy.init_node("teleopCtrl", anonymous=False)

        self.pub = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10, latch=True)
        rospy.Subscriber("/turtle1/cmd_vel", Twist, self.callback)

    def callback(self, data):
        if data.linear.x == 2:
            if self.running == 0:
                cmd.roboEmFrente()
                self.running = 1
            else:
                self.running = 0
                cmd.roboParar()
        elif data.linear.x == -2:
            if self.running == 0:
                cmd.roboParaTras()
                self.running = 1
            else:
                self.running = 0
                cmd.roboParar()
        elif data.angular.z == 2:
            if self.running == 0:
                cmd.roboEsq()
                self.running = 1
            else:
                self.running = 0
                cmd.roboParar()
        elif data.angular.z == -2:
            if self.running == 0:
                cmd.roboDir()
                self.running = 1
            else:
                self.running = 0
                cmd.roboParar()




if __name__ == "__main__":
    tele = TeleopCtrl()
    cmd = cmdMotores.CmdMotores(tele.pub)
    rospy.spin()
