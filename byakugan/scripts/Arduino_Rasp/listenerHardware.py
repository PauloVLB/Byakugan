#!/usr/bin/env python

import rospy
import cv2
import message_filters
from std_msgs.msg import Float64MultiArray
from byakugan.msg import SensoresDistanciaMsg, RefletanciaMsg

def callbackHardware(refle, dist):
    rospy.loginfo('refletancia ' + str(refle.refletancia))
    rospy.loginfo('distancia ' + str(dist.sensoresDistancia))

def listenerHardware():
    rospy.init_node('listenerHardware', anonymous=True)
    subRefle = message_filters.Subscriber('refletancia', RefletanciaMsg)
    subDistancia = message_filters.Subscriber('distancia', SensoresDistanciaMsg)

    ts = message_filters.TimeSynchronizer([subRefle, subDistancia], 10)
    ts.registerCallback(callbackHardware)

    rospy.spin()

if __name__ == "__main__":
	try:
		listenerHardware()
	except rospy.ROSInterruptException:
		pass
