#!/usr/bin/env python
# Libraries 
import rospy 
import time 
from std_msgs.msg import Int16 
import RPi.GPIO as GPIO

# Motor_Libraries
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import atexit

# Set the GPIO modes 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

# Index of wheels
#######
#Back##
#3   4#
#     #
#2   1#
#Head##
#######

##########################

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# motor: recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

def callback_1(data): 
	rospy.loginfo('Distance(UltraSonic_1): %s', data.data)
	UltraSonic_1 = data.data;
def callback_2(data): 
	rospy.loginfo('Distance(UltraSonic_2): %s', data.data)
	UltraSonic_2 = data.data;
def callback_3(data): 
	rospy.loginfo('Distance(UltraSonic_3): %s', data.data)
	UltraSonic_3 = data.data;
		
def listener(): 
	rospy.init_node('UltraSonic_Listener_Node', anonymous = False) 
	rospy.Subscriber('UltraSonic_Talker_First', Int16, callback_1)
	rospy.Subscriber('UltraSonic_Talker_Second', Int16, callback_2)
	rospy.Subscriber('UltraSonic_Talker_Third', Int16, callback_3)
	
	print('Subscriber Created')

	rospy.spin() # Forever

#Get_Motor_num
myMotor_1 = mh.getMotor(1)
myMotor_2 = mh.getMotor(2)
myMotor_3 = mh.getMotor(3)
myMotor_4 = mh.getMotor(4)
UltraSonic_1 = 0;
UltraSonic_2 = 0;
UltraSonic_3 = 0;


if __name__ == '__main__': 
	try: 
		print('Initialing') 
		listener() 
	except rospy.ROSInterruptException: 
		pass
