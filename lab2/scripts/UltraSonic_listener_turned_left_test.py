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
#Head##
#1   2#
#     #
#4   3#
#Back##
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

def Turned_Left():
	print ("Turned left!! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.FORWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.FORWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(70)
	myMotor_2.setSpeed(90)
	myMotor_3.setSpeed(90)
	myMotor_4.setSpeed(70)
	time.sleep(0.01)
	
def callback_1(data): 
	#rospy.loginfo('Distance(UltraSonic_1): %s', data.data)
	UltraSonic_1 = data.data;
def callback_2(data): 
	#rospy.loginfo('Distance(UltraSonic_2): %s', data.data)
	UltraSonic_2 = data.data;
def callback_3(data): 
	#rospy.loginfo('Distance(UltraSonic_3): %s', data.data)
	UltraSonic_3 = data.data;
	Turned_Left();
		
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
