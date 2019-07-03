#!/usr/bin/env python
# -*- coding: utf8 -*-

import rospy
import cv2
from std_msgs.msg import Int32MultiArray
import message_filters

'''
def cbAtuantes(motores, garras):


    img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
    cv2.imshow('frame', img)
    cv2.waitKey(1)
'''

def cbMotores(data):
    print 'cbMotores'
    img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
    cv2.imshow('frame', img)
    cv2.waitKey(1)

def cbGarras(data):
    print 'cbGarras'
    img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
    cv2.imshow('frame', img)
    cv2.waitKey(1)

def run():

    rospy.init_node('atuantesGUI', anonymous=False)

    subMotores = message_filters.Subscriber("ctrl_motores", Int32MultiArray)
    subGarras = message_filters.Subscriber("ctrl_garras", Int32MultiArray)

    subMotores.registerCallback(cbMotores)
    subGarras.registerCallback(cbGarras)
    
    '''
    ts = message_filters.TimeSynchronizer([subMotores, subGarras], 10)
    ts.registerCallback(cbAtuantes)
    '''

    rospy.spin()

if __name__ == "__main__":
    try:
        run()
    except:
        pass
