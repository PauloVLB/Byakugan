#!/usr/bin/env python

import rospy
import threading
from std_msgs.msg import Int32MultiArray
from SensorsListener import SensorsListener
import refletancia
from Sensores import Sensores
#import motores

def acionarMotores(esq, dir):
    dataMotores.data = [esq, dir]
    pubMotores.publish(dataMotores)
    rate.sleep()

def showValue():
    while not rospy.is_shutdown():
        if refle.b_b_b_b():
            acionarMotores(45, 45)
        elif refle.b_p_b_b():
            acionarMotores(-45, 45)
        elif refle.b_b_p_b():
            acionarMotores(45, -45)

        elif refle.p_p_b_b() or refle.p_p_p_b():
            while not refle.esqBranco():
                acionarMotores(45, 45)
            while refle.esqBranco():
                acionarMotores(-45, 45)
            while not refle.esqBranco():
                acionarMotores(-45, 45)
            while not refle.dirBranco():
                acionarMotores(45, -45)


        elif refle.b_b_p_p() or refle.b_p_p_p():
            while not refle.dirBranco():
                acionarMotores(45, 45)
            while refle.dirBranco():
                acionarMotores(45, -45)
            while not refle.dirBranco():
                acionarMotores(45, -45)
            while not refle.esqBranco():
                acionarMotores(-45, 45)

        rate.sleep()

if __name__ == "__main__":
    try:
        rospy.init_node('testeEstrategia', anonymous=True)
        rate = rospy.Rate(230)
        pubMotores = rospy.Publisher("ctrl_motores", Int32MultiArray, queue_size=10)
        sl = SensorsListener()
        refle = refletancia.Refletancia(sl)
        threading.Thread(target=showValue).start()
        sl.register()

    except rospy.ROSInterruptException:
        pass
