#!/usr/bin/env python

import rospy
import threading
from SensorsListener import SensorsListener
from Sensores import Sensores


def showValue():
    while not rospy.is_shutdown():
        rospy.loginfo(sl.getRefle(0))
        #rospy.loginfo(sl.getDist(0))
        #rospy.loginfo(sl.getBtn3())

if __name__ == "__main__":
    try:
        rospy.init_node('testeEstrategia', anonymous=True)
        sl = SensorsListener()
        threading.Thread(target=showValue).start()
        sl.register()

    except rospy.ROSInterruptException:
        pass
