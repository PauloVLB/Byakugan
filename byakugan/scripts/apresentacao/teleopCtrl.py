#!/usr/bin/env python

import sys
sys.path.append('../atuadores')
import motores

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

def acionarMotores(esq, dir):
        motores.data = [esq, dir]
        pubMotores.publish(motores)

def callback(data):
    if data.linear.x == 2:
        acionarMotores(30, 30)
    elif data.linear.x == -2:
        acionarMotores(-30, -30)
    elif data.angular.z == 2:
        acionarMotores(-30, 30)
    elif data.angular.z == -2:
        acionarMotores(30, -30)

def loop():
    pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)

    rospy.Subscriber("/turtle1/cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node("teleop", anonymous=True)
    pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
    motores = motores.Motores()
    loop()
