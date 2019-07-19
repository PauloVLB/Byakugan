#!/usr/bin/env python

import rospy
import motores
from geometry_msgs.msg import Twist

def callback(data):
    if data.linear.x == 2:
        motores.roboEmFrente(2)
    elif data.linear.x == -2:
        motores.roboParaTras(2)
    elif data.angular.z == 2:
        motores.roboEsq(2)
    elif data.angular.z == -2:
        motores.roboDir(2)

def loop():
    rospy.Subscriber("/turtle1/cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == "__main__":
    motores = motores.Motores()
    loop()
