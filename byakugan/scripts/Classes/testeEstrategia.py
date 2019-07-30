#!/usr/bin/env python

import rospy
import threading
from std_msgs.msg import Int32MultiArray
from SensorsListener import SensorsListener
from Sensores import Sensores
#import motores


def maisEsqBranco():
    return sl.getRefle(0) > 4
def esqBranco():
    return sl.getRefle(1) > 4
def dirBranco():
    return sl.getRefle(2) > 4
def maisDirBranco():
    return sl.getRefle(3) > 4

def b_b_b_b():
    return maisEsqBranco() and esqBranco() and dirBranco() and maisDirBranco()

def p_p_p_p():
    return not maisEsqBranco() and not esqBranco() and not dirBranco() and not maisDirBranco()

def p_b_b_b():
    return not maisEsqBranco() and esqBranco() and dirBranco() and maisDirBranco()

def p_p_b_b():
    return not maisEsqBranco() and not esqBranco() and dirBranco() and maisDirBranco()

def p_p_p_b():
    return not maisEsqBranco() and not esqBranco() and not dirBranco() and maisDirBranco()

def b_p_p_p():
    return maisEsqBranco() and not esqBranco() and not dirBranco() and not maisDirBranco()

def b_b_p_p():
    return maisEsqBranco() and esqBranco() and not dirBranco() and not maisDirBranco()

def b_b_b_p():
    return maisEsqBranco() and esqBranco() and dirBranco() and not maisDirBranco()

def p_b_p_b():
    return not maisEsqBranco() and esqBranco() and not dirBranco() and maisDirBranco()

def p_b_b_p():
    return not maisEsqBranco() and esqBranco() and dirBranco() and not maisDirBranco()

def b_p_b_p():
    return maisEsqBranco() and not esqBranco() and dirBranco() and not maisDirBranco()

def b_p_p_b():
    return maisEsqBranco() and not esqBranco() and not dirBranco() and maisDirBranco()

def p_b_p_p():
    return not maisEsqBranco() and esqBranco() and not dirBranco() and not maisDirBranco()

def p_p_b_p():
    return not maisEsqBranco() and not esqBranco() and dirBranco() and not maisDirBranco()

def b_p_b_b():
    return maisEsqBranco() and not esqBranco() and dirBranco() and maisDirBranco()

def b_b_p_b():
    return maisEsqBranco() and esqBranco() and not dirBranco() and maisDirBranco()

def acionarMotores(esq, dir):
    dataMotores.data = [esq, dir]
    pubMotores.publish(dataMotores)
    rate.sleep()

def showValue():
    while not rospy.is_shutdown():
        if b_b_b_b():
            acionarMotores(45, 45)
        elif b_p_b_b():
            acionarMotores(-45, 45)
        elif b_b_p_b():
            acionarMotores(45, -45)

        elif p_p_b_b() or p_p_p_b():
            while not esqBranco():
                acionarMotores(45, 45)
            while esqBranco():
                acionarMotores(-45, 45)
            while not esqBranco():
                acionarMotores(-45, 45)
            while not dirBranco():
                acionarMotores(45, -45)


        elif b_b_p_p() or b_p_p_p():
            while not dirBranco():
                acionarMotores(45, 45)
            while dirBranco():
                acionarMotores(45, -45)
            while not dirBranco():
                acionarMotores(45, -45)
            while not esqBranco():
                acionarMotores(-45, 45)

        rate.sleep()

if __name__ == "__main__":
    try:
        rospy.init_node('testeEstrategia', anonymous=True)
        dataMotores = Int32MultiArray()
        rate = rospy.Rate(230)
        pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        sl = SensorsListener()
        threading.Thread(target=showValue).start()
        sl.register()

    except rospy.ROSInterruptException:
        pass
