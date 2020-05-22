#!/usr/bin/env python

# Libraries
import rospy
import time
import atexit
#from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from std_msgs.msg import Int16
import RPi.GPIO as GPIO

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##########################

# create a default object, no changes to I2C address or frequency
#mh = Raspi_MotorHAT(addr=0x6f)

# motor: recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

def motor_go():
	for i in range(100):
		myMotor.setSpeed(i)
		time.sleep(0.01)

# Index of wheels
#####
#Back#
#3   4#
#     #
#2   1#
#Head#
#####
def callback(data):
    rospy.loginfo('Distance: %s', data.data)
    
'''
def controlDirection():
	# Direction of wheels.
    myMotor_1.run(Raspi_MotorHAT.BACKWARD)
	myMotor_2.run(Raspi_MotorHAT.BACKWARD)
	myMotor_3.run(Raspi_MotorHAT.BACKWARD)
	myMotor_4.run(Raspi_MotorHAT.BACKWARD)
	
	if(data.data < 5):
		# Turn right
		myMotor_1.setSpeed(140)
		myMotor_2.setSpeed(0)
		myMotor_3.setSpeed(0)
		myMotor_4.setSpeed(140)
		time.sleep(0.01)
'''

def listener():
    rospy.init_node('UltraSonic_Listener_Node', anonymous = False)
    #rospy.Subscriber('UltraSonic_Talker_First', Int16, callback)
    rospy.Subscriber('UltraSonic_Talker_Second', Int16, callback)
    #rospy.Subscriber('UltraSonic_Talker_Third', Int16, callback)
    
    print('Subscriber Created')
    rospy.spin() # Forever

if __name__ == '__main__':
    try:
        print('Initialing')
        listener()
    except rospy.ROSInterruptException:
        pass
