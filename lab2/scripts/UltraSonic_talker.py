#!/usr/bin/env python

# Libraries 
import rospy 
from std_msgs.msg import Int16 
import time, atexit 
import RPi.GPIO as GPIO

# Set the GPIO modes 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

##########################
def talker(): 
    rospy.init_node('UltraSonic_Talker_Node', anonymous = False) 
    rate = rospy.Rate(10)
    
    myTopic = rospy.get_param("~my_topic")
    trigger_pin = rospy.get_param("~GPIO_TRIGGER")
    echo_pin = rospy.get_param("~GPIO_ECHO")
    
#    trigger_pin = 18 	# transmit
#    echo_pin = 24 		# receive
    GPIO.setup(trigger_pin, GPIO.OUT) 
    GPIO.setup(echo_pin, GPIO.IN)
    
    pub = rospy.Publisher(myTopic , Int16, queue_size = 10, tcp_nodelay = True) 
    print('Publisher Created')
    
    while not rospy.is_shutdown(): 
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

		# save StartTime 
		while GPIO.input(echo_pin) == 0: 
			StartTime = time.time() 
			#print("0")
		# save time of arrival 
		while GPIO.input(echo_pin) == 1: 
			StopTime = time.time() 
			#print("1")
		# time difference between start and arrival 
		TimeElapsed = StopTime - StartTime 
		# multiply with the sonic speed (34300 cm/s) 
		# and divide by 2, because there and back 
		distance = (TimeElapsed * 34300) / 2 
		pub_str = "%s Distance is : %s" % (rospy.get_caller_id(), distance) 
		print(pub_str)
		pub.publish(distance)

		rate.sleep()

if __name__ == '__main__': 
    try:
        print 'Initialing' 
        talker() 
    except rospy.ROSInterruptException: 
        pass
