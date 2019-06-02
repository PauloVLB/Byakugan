#!/usr/bin/env python

import rospy
import sys
from std_msgs.msg import Float64MultiArray
from serial import Serial

def enviarSerial(data):
	x,y,w,h = getCoordenadas(data.data)
		
	angulo = toAngulo(x + (h/2))
	enviando = str(int(angulo))
	nBytes = serial.in_waiting

	if (nBytes > 0):
		serial.read(1)
		serial.write(enviando)
		rospy.loginfo('ENVIADO')
	else:
		rospy.loginfo('Nada enviado')

	rospy.loginfo('tentou enviar: ' + enviando)
	rospy.loginfo('nBytes: ' + str(nBytes))

def listenerCoordenadas():
	rospy.init_node('anguloSerial', anonymous=True)
	rospy.Subscriber('coordenadas_detectadas', Float64MultiArray, enviarSerial)
	rospy.spin()


def configSerial(args): 
	nomePorta = '/dev/ttyUSB0'
	if (len(args) > 2):
		nomePorta = args[1]

	serial.port = nomePorta
	serial.baudrate = 9600
	#serial.timeout = 1
	#serial.inter_byte_timeout = 0.005
	#serial.bytesize = 8
	serial.open()

def getCoordenadas(data):
	x = data[0]
	y = data[1]
	w = data[2]
	h = data[3]

	return (x,y,w,h)

def toAngulo(coordenada):
	return (180 * coordenada)/640 

if __name__ == "__main__":
	arrayCoordenadas = Float64MultiArray()
	arrayCoordenadas.data = [0,0,0,0]

	serial = Serial()
	configSerial(sys.argv)
	
	listenerCoordenadas()