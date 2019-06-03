#!/usr/bin/env python

import rospy
import message_filters
import cv2
from std_msgs.msg import Int32MultiArray, Float64MultiArray
from sensor_msgs.msg import Image
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg, BoolStamped, BotoesMsg
from cv_bridge import CvBridge

pubMotores = rospy.Publisher('motores', Int32MultiArray, queue_size=10)
pubGarra = rospy.Publisher('garra', Int32MultiArray, queue_size=10)

def map(x, in_min, in_max, out_min, out_max):
    if (x > in_max):
        x = in_max

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def arduinoCamCb(refle, dist, circulo, botoes, coordenadas):

    maisEsq = refle.refletancia[0]
    esq = refle.refletancia[1]
    dir = refle.refletancia[2]
    maisDir = refle.refletancia[3]

    distFrontal =  dist.sensoresDistancia[0]
    distEsq = dist.sensoresDistancia[1]
    distDir = dist.sensoresDistancia[2]

    if botoes.botao1.data:
        print 'botao 1 pressionado'
    if botoes.botao2.data:
        print 'botao 2 pressionado'
    if botoes.botao3.data:
        print 'botao 3 pressionado'

    if circulo.existe.data:
        dataMotores.data = [25,-25]
        ang = map(coordenadas.data[0], 0, 480, 0, 180)
        dataGarra.data = [ang, ang]
    else:
        dataMotores.data = [0,0]
        dataGarra.data = [0, 0]

    pubGarra.publish(dataGarra)
    pubMotores.publish(dataMotores)

def arduino_cam():
    rospy.init_node('arduino_cam', anonymous=True)
    subBotoes = message_filters.Subscriber('botoes', BotoesMsg)
    subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
    subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)
    subCam = message_filters.Subscriber('tem_circulos', BoolStamped)
    subCoordenadas = message_filters.Subscriber('/coordenadas_circulos', Float64MultiArray)

    ts = message_filters.TimeSynchronizer([subRefle, subDistancia, subCam, subBotoes], 20)

    ts.registerCallback(arduinoCamCb)

    rospy.spin()

if __name__ == "__main__":
    try:
        ponte = CvBridge()
        coordenadas = Float64MultiArray()
        coordenadas.data = [0,0,0,0]

        dataGarra = Int32MultiArray()
        dataGarra.data = [0, 0]
        dataMotores = Int32MultiArray()
        dataMotores.data = [0, 0]
        arduino_cam()
    except rospy.ROSInterruptException:
        pass