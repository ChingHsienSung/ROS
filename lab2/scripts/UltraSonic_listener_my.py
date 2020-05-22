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
#motor##sensor#
#Head####Head##
#1   2###  1  #
#     ###    2#
#4   3###    3#
#Back####Back##
##############

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
	myMotor_1.setSpeed(60)
	myMotor_2.setSpeed(110)
	myMotor_3.setSpeed(110)
	myMotor_4.setSpeed(60)
	time.sleep(0.01)
def Turned_Right():
	print ("Turned right! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.FORWARD)
	myMotor_3.run(Raspi_MotorHAT.FORWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(110)
	myMotor_2.setSpeed(60)
	myMotor_3.setSpeed(60)
	myMotor_4.setSpeed(110)
	time.sleep(0.01)

def callback_1(data): 
	global UltraSonic_1
	#rospy.loginfo('Distance(UltraSonic_1): %s', data.data)
	UltraSonic_1 = data.data
def callback_2(data): 
	global UltraSonic_2
	#rospy.loginfo('Distance(UltraSonic_2): %s', data.data)
	UltraSonic_2 = data.data
def callback_3(data): 
	global UltraSonic_3
	global X_left, X_right, X_diff
	global Car_state
	global pub
	#rospy.loginfo('Distance(UltraSonic_3): %s', data.data)
	
	UltraSonic_3 = data.data
	
	#State machine
	if(Car_state == S_left):	
		Turned_Left()
		if(UltraSonic_1 > 15):	
			if(UltraSonic_2 > UltraSonic_3):
				if(UltraSonic_2 > 8):
					Car_state = S_right
				else:
					Car_state = S_left
			else:
				if(UltraSonic_3 > 8):
					Car_state = S_left
				else:
					Car_state = S_right
		else:
			Car_state = S_left
	elif(Car_state == S_right):
		Turned_Right()
		if(UltraSonic_1 > 15):	
			if(abs(UltraSonic_2 - UltraSonic_3) > 25):
				Car_state = S_right
			else:
				if(UltraSonic_2 > UltraSonic_3):
					if(UltraSonic_2 > 8):
						Car_state = S_right
					else:
						Car_state = S_left
				else:
					if(UltraSonic_3 > 8):
						Car_state = S_left
					else:
						Car_state = S_right
		else:
			Car_state = S_left
	else:
		Car_state = S_left
		Turned_Left()
	
	
	
	
	pub.publish(Car_state)
		
def listener(): 
	rospy.init_node('UltraSonic_Listener_Node', anonymous = False) 
	rospy.Subscriber('UltraSonic_Talker_First', Int16, callback_1)
	rospy.Subscriber('UltraSonic_Talker_Second', Int16, callback_2)
	rospy.Subscriber('UltraSonic_Talker_Third', Int16, callback_3)
	
	print('type(pub) = ', type(pub))
	print('Subscriber Created')

	rospy.spin() # Forever

#Get_Motor_num
myMotor_1 = mh.getMotor(1)
myMotor_2 = mh.getMotor(2)
myMotor_3 = mh.getMotor(3)
myMotor_4 = mh.getMotor(4)
#declare sensor variable and input control
UltraSonic_1 = 0
UltraSonic_2 = 0
UltraSonic_3 = 0
X_left = 0
X_right = 0
X_diff = 0
#declare 
Car_state = 0
S_left = 0b0
S_right = 0b1

pub = rospy.Publisher('UltraSonic_Listener_Node', Int16, queue_size = 10, tcp_nodelay = True) 
if __name__ == '__main__': 
	try: 
		print('Initialing') 
		listener() 
	except rospy.ROSInterruptException: 
		pass
