#!/usr/bin/env python

import rospy
import threading
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

def showValue():
    while not rospy.is_shutdown():
        pass
if __name__ == "__main__":
    try:
        rospy.init_node('testeEstrategia', anonymous=True)
        sl = SensorsListener()
        threading.Thread(target=showValue).start()
        sl.register()

    except rospy.ROSInterruptException:
        pass
