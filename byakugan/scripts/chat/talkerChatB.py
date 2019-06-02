#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

def callback(data):
	print data.data

def talker():

	pub = rospy.Publisher("chatB", String, queue_size=10)
	rospy.init_node("talkerChatB", anonymous=False)
	rospy.Subscriber("chatA", String, callback)
	rate = rospy.Rate(20)

	print 'nome:'
	name = raw_input()

	while not rospy.is_shutdown():

		msg = raw_input()
		msg_result = name + ": " + msg
		pub.publish(msg_result)
	
	rospy.spin()

if __name__ == "__main__":
	talker()