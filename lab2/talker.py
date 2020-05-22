#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Int16
import RPi.GPIO as GPIO
# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Set variable for the GPIO RedLight pin
pinRedLight = 4
# Set the GPIO pin mode to be Input
GPIO.setup(pinRedLight, GPIO.IN)
##########################
def talker():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('chatter', Int16, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        light_value = GPIO.input(pinRedLight)
        light_str = "%s Light Value is : %s" % (rospy.get_caller_id(), light_value)
        rospy.loginfo(light_str)
        pub.publish(light_value)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
