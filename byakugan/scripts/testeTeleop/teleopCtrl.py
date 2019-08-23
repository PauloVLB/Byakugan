#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from byakugan.msg import CtrlMotores
import cmdMotores

def callback(data):
    if data.linear.x == 2:
        cmd.roboEmFrente(.5)
    elif data.linear.x == -2:
        cmd.roboParaTras(.5)
    elif data.angular.z == 2:
        cmd.roboEsq(.5)
    elif data.angular.z == -2:
        cmd.roboDir(.5)

rospy.init_node("teleopCtrl", anonymous=False)
pub = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10, latch=True)
rospy.Subscriber("/turtle1/cmd_vel", Twist, callback)


if __name__ == "__main__":
    cmd = cmdMotores.CmdMotores(pub)
    rospy.spin()
