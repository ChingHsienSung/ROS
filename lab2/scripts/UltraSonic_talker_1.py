#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Libraries
import rospy
from std_msgs.msg import Int16
import time, atexit, os
import RPi.GPIO as GPIO

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#######################
def kill():
	os.system("kill -KILL " + str(os.getpid()))

def resetUltraSoinc(echo_pin):
	resetPin = echo_pin

	GPIO.setup(resetPin, GPIO.OUT)
	time.sleep(0.00001)

	GPIO.output(resetPin, GPIO.LOW)
	time.sleep(0.00001)

	GPIO.setup(resetPin, GPIO.IN)
	time.sleep(0.00001)

	rospy.loginfo("***** Reset! *****")
	pass


def talker():
	rospy.init_node('UltraSonic_Talker_Node', anonymous = False)
	rospy.on_shutdown(kill)
	rate = rospy.Rate(10)

	myTopic = "UltraSonic_Talker_First"
	# GPIO pin
	trigger_pin = 25 #18
	echo_pin = 23	#24

	GPIO.setup(trigger_pin, GPIO.OUT)
	GPIO.setup(echo_pin, GPIO.IN)

	pub = rospy.Publisher(myTopic, Int16, queue_size = 1, tcp_nodelay = True)
	print('Publisher Created')


	while not rospy.is_shutdown():
		isReseted = False
		# set Trigger to LOW
		GPIO.output(trigger_pin, GPIO.LOW)
		time.sleep(0.000005)

		# set Trigger after 5us to HIGH
		GPIO.output(trigger_pin, GPIO.HIGH)
		# set Trigger after 10us to LOW

		time.sleep(0.00001)
		GPIO.output(trigger_pin, GPIO.LOW)

		StartTime = time.time()
		StopTime = time.time()

		# save time of StartTime
		while (GPIO.input(echo_pin) == 0):
			StartTime = time.time()
			if (StartTime - StopTime > 0.5):
				resetUltraSoinc(echo_pin)
				isReseted = True
				break

			if (isReseted == True):
				continue

		# save time of StopTime
		while (GPIO.input(echo_pin) == 1):
			StopTime = time.time()
			if (StopTime - StartTime > 0.5):
				resetUltraSoinc(echo_pin)
				isReseted = True
				break

		if (isReseted == True):
			continue

		TimeElapsed = StopTime - StartTime
		distance = (TimeElapsed * 34300) / 2
		pub_str = "%s Distance is :%s" % (rospy.get_caller_id(), distance)
		rospy.loginfo(pub_str)
		pub.publish(distance)

		rate.sleep()

if __name__ == '__main__':
	try:
		print('Initialing')
		talker()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
