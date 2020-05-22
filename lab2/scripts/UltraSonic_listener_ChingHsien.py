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
	#print ("Go straight! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	
	#Set Motor Speed
	# Set the distance
	
	if(right_front_dis > right_back_dis and (right_front_dis - right_back_dis) > 0.01):
		# Turn left slightly
		myMotor_1.setSpeed(100)
		myMotor_2.setSpeed(50)
		myMotor_3.setSpeed(50)
		myMotor_4.setSpeed(100)
	elif(right_front_dis < right_back_dis and (right_back_dis - right_front_dis) > 0.01):
		# Turn right slightly
		myMotor_1.setSpeed(50)
		myMotor_2.setSpeed(100)
		myMotor_3.setSpeed(100)
		myMotor_4.setSpeed(50)	
	else:
		if(right_front_dis < 7 or right_back_dis < 7):
			# Turn left strongly
			myMotor_1.setSpeed(30)
			myMotor_2.setSpeed(120)
			myMotor_3.setSpeed(120)
			myMotor_4.setSpeed(30)
		elif(right_front_dis > 7 or right_back_dis > 7):
			# Turn right strongly
			myMotor_1.setSpeed(120)
			myMotor_2.setSpeed(30)
			myMotor_3.setSpeed(30)
			myMotor_4.setSpeed(120)
		else:
			# Move forward(go straight)
			myMotor_1.setSpeed(70)
			myMotor_2.setSpeed(70)
			myMotor_3.setSpeed(70)
			myMotor_4.setSpeed(70)
	time.sleep(0.01)

def turnLeft():
	#print ("Turned left!! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.FORWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.FORWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(80)
	myMotor_2.setSpeed(80)
	myMotor_3.setSpeed(80)
	myMotor_4.setSpeed(80)
	time.sleep(0.01)

def turnRight():
	#print ("Turned right! ")
	#Set Motor Direction
	myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.FORWARD)
	myMotor_3.run(Raspi_MotorHAT.FORWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	#Set Motor Speed
	myMotor_1.setSpeed(80)
	myMotor_2.setSpeed(80)
	myMotor_3.setSpeed(80)
	myMotor_4.setSpeed(80)
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

	# Make sure the input of current state.
	# 0: Far from wall. 
	# 1: Close to wall.
	front_sensor       = 1 if (UltraSonic_1 < 12) else 0
	right_front_sensor = 1 if (UltraSonic_2 < 30) else 0
	right_back_sensor  = 1 if (UltraSonic_3 < 30) else 0


	# motion_state: 0 => Go straight
	#		 		1 => Turn left
	#		 		2 => Turn right

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
	
	# Turn right
	else:
		if(front_sensor == 0 and right_front_sensor == 1 and right_back_sensor == 1):
			goStraight(UltraSonic_2, UltraSonic_3)
			motion_state = 0
		else:
			# Go straight and turn right aat the same time.
			goStraight(UltraSonic_2, UltraSonic_3)
			turnRight()
			motion_state = 2


def listener(): 
	rospy.init_node('UltraSonic_Listener_Node', anonymous = False) 
	rospy.Subscriber('UltraSonic_Talker_First', Int16, callback_1)
	rospy.Subscriber('UltraSonic_Talker_Second', Int16, callback_2)
	rospy.Subscriber('UltraSonic_Talker_Third', Int16, callback_3)
	
	print('Subscriber Created')

	# Keep executing the node function.
	rospy.spin() # Forever

# Get_Motor_num
myMotor_1 = mh.getMotor(1)
myMotor_2 = mh.getMotor(2)
myMotor_3 = mh.getMotor(3)
myMotor_4 = mh.getMotor(4)
# Declare sensor variable and input control.
UltraSonic_1 = 0
UltraSonic_2 = 0
UltraSonic_3 = 0
# The initial motion state is go straight. 
motion_state = 0

if __name__ == '__main__': 
	try: 
		print('Initialing') 
		listener() 
	except rospy.ROSInterruptException: 
		pass
