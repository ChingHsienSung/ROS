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

def goStraight(right_front_dis, right_back_dis):
	print ("Go straight! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	
	#Set Motor Speed
	if(right_front_dis > right_back_dis):
		myMotor_1.setSpeed(120)
		myMotor_2.setSpeed(30)
		myMotor_3.setSpeed(30)
		myMotor_4.setSpeed(120)
	elif(right_front_dis < right_back_dis):
		myMotor_1.setSpeed(30)
		myMotor_2.setSpeed(120)
		myMotor_3.setSpeed(120)
		myMotor_4.setSpeed(30)	
	else:
		myMotor_1.setSpeed(80)
		myMotor_2.setSpeed(80)
		myMotor_3.setSpeed(80)
		myMotor_4.setSpeed(80)
	time.sleep(0.01)

def turnLeftSlightly():
	print ("Turned_Left_Slightly!! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(20)
	myMotor_2.setSpeed(70)
	myMotor_3.setSpeed(70)
	myMotor_4.setSpeed(20)
	time.sleep(0.01)

def turnRightSlightly():
	print ("Turned_Right_Slightly!! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(20)
	myMotor_2.setSpeed(70)
	myMotor_3.setSpeed(70)
	myMotor_4.setSpeed(20)
	time.sleep(0.01)

def turnLeft():
	print ("Turned left!! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.FORWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.FORWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(70)
	myMotor_2.setSpeed(70)
	myMotor_3.setSpeed(70)
	myMotor_4.setSpeed(70)
	time.sleep(0.01)

def turnRight():
	print ("Turned right! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.FORWARD)
	myMotor_3.run(Raspi_MotorHAT.FORWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(70)
	myMotor_2.setSpeed(70)
	myMotor_3.setSpeed(70)
	myMotor_4.setSpeed(70)
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
	global motion_state
	#rospy.loginfo('Distance(UltraSonic_3): %s', data.data)
	
	# Read the data
	UltraSonic_3 = data.data

	# Make sure the current state of input.
	# 0: Far from wall. 
	# 1: Close to wall.
	front_sensor       = 1 if (UltraSonic_1 < 10) else 0
	right_front_sensor = 1 if (UltraSonic_2 < 10) else 0
	right_back_sensor  = 1 if (UltraSonic_3 < 10) else 0


	# motion_ state: 0 => Turn left slightly
	#				 1 => Turn right slightly
	#		 		 2 => Turn left
	#		 		 3 => Turn right
	xin = front_sensor*4 + right_front_sensor*2 + right_back_sensor
	if(motion_state == 0):	#Turn left slightly
		if(xin == 0):
			motion_state = 3
		elif(xin == 1):
			motion_state = 1	
		elif(xin == 2 or xin == 3):
			motion_state = 0
		else:
			motion_state = 2
	elif(motion_state == 1):
		if(xin == 0):
			motion_state = 3
		elif(xin == 1 or xin == 3):
			motion_state = 1
		elif(xin == 2):
			motion_state = 0
		else:
			motion_state = 2
	elif(motion_state == 2):
		if(xin == 0):
			motion_state = 3
		elif(xin == 2 or xin == 3):
			motion_state = 0
		else:
			motion_state = 2
	else:
		if(xin == 0):
			motion_state = 3
		elif(xin == 1 or xin == 3):
			motion_state = 1
		elif(xin == 2):
			motion_state = 0
		else:
			motion_state = 2
	
	if(motion_state == 0):
		turnLeftSlightly()
	elif(motion_state == 1):
		turnRightSlightly()
	elif(motion_state == 2):
		turnLeft()
	else:
		turnRight()
		
	"""
	# Go straight
	if(motion_state == 0):
		if(front_sensor == 0 and right_front_sensor == 0 and right_back_sensor == 0):
			turnRight()
			motion_state = 2
		
		elif(front_sensor == 1 and right_front_sensor == 1 and right_back_sensor == 1):
			turnLeft()
			motion_state = 1
		else:
			goStraight(UltraSonic_2, UltraSonic_3)
			motion_state = 0

	# Turn left
	elif(motion_state == 1):
		if(front_sensor == 0 and right_front_sensor == 1 and right_back_sensor == 1):
			goStraight(UltraSonic_2, UltraSonic_3)
			motion_state = 0
		else:
			turnLeft()
			motion_state = 1
	
	# Turn right (state = 2)
	else:
		if(front_sensor == 0 and right_front_sensor == 1 and right_back_sensor == 1):
			goStraight(UltraSonic_2, UltraSonic_3)
			motion_state = 0
		else:
			goStraight(UltraSonic_2, UltraSonic_3)
			turnRight()
			motion_state = 2
	"""
		
def listener(): 
	rospy.init_node('UltraSonic_Listener_Node', anonymous = False) 
	rospy.Subscriber('UltraSonic_Talker_First', Int16, callback_1)
	rospy.Subscriber('UltraSonic_Talker_Second', Int16, callback_2)
	rospy.Subscriber('UltraSonic_Talker_Third', Int16, callback_3)
	
	print('Subscriber Created')

	# Keep executing the node function.
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
#declare 
motion_state = 0

if __name__ == '__main__': 
	try: 
		print('Initialing') 
		listener() 
	except rospy.ROSInterruptException: 
		pass
