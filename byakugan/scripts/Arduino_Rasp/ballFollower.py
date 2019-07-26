#!/usr/bin/env python

import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Vector3Stamped
from byakugan.msg import SensoresDistanciaMsg, BoolStamped, BotoesMsg

pubMotores = rospy.Publisher('ctrl_motores', Int32MultiArray, queue_size=10)

angAnt = 0
velAnt = 0
def map(x, in_min, in_max, out_min, out_max):
    if (x > in_max):
        x = in_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def acionarMotores(esq, dir):
    dataMotores.data = [esq, dir]

    pubMotores.publish(dataMotores)

def callback(botoes, circulo, coordenadas):
    if botoes.botao2.data:
        acionarMotores(25, -25)
    else:
        acionarMotores(0, 0)

def ballFollower():
    rospy.init_node('ballFollower', anonymous=True)

    subBotoes = message_filters.Subscriber('botoes', BotoesMsg)
    subCam = message_filters.Subscriber('tem_circulos', BoolStamped)
    subCoordenadas = message_filters.Subscriber('coordenadas_circulos', Vector3Stamped)

    ts = message_filters.TimeSynchronizer([subBotoes, subCam, subCoordenadas], 20)

    ts.registerCallback(callback)

    rospy.spin()

if __name__ == "__main__":
    try:
        dataMotores = Int32MultiArray()
        dataMotores.data = [0, 0]
        ballFollower()
    except rospy.ROSInterruptException:
        pass
