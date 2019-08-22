#!/usr/bin/env python
import time
from osr_msgs.msg import Joystick, Commands, Encoder
import rospy
from robot import Robot
import message_filters


global encs
global osr

encs = [0]*4

def joy_callback(message):
	global encs
	cmds = Commands()
	out_cmds = osr.generateCommands(message.vel,message.steering,encs)
	cmds.drive_motor  = out_cmds[0]
	cmds.corner_motor = out_cmds[1]
	try:
		pub.publish(cmds)
	except:
		pass

def enc_callback(message):
	global encs
	temp = [0]*4
	for i in range(4):
		temp[i] = message.abs_enc[i] + 1
	encs = temp

if __name__ == '__main__':
	while not(rospy.get_param("controller_init")):
		time.sleep(0.1)

	rospy.init_node('rover')
	rospy.loginfo("Starting the rover node")
	osr = Robot()
	global pub
	joy_sub = rospy.Subscriber("/joystick",Joystick, joy_callback)
	enc_sub  = rospy.Subscriber("/encoder", Encoder, enc_callback)
	rate = rospy.Rate(10)
	#time_sync = message_filters.TimeSynchronizer([joy_sub, mc_sub],10)
	#time_sync.registerCallback(callback)

	pub = rospy.Publisher("/robot_cmds", Commands, queue_size = 1)
	rate.sleep()
	rospy.spin()


