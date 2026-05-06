#!/usr/bin/env python3

import rospy, roslaunch, yaml, rospkg
import os, signal, subprocess

from std_msgs.msg import String

from bot_msgs.srv import SaveMap, SaveMapResponse
from cartographer_ros_msgs.srv import WriteState


# H/W info & Path Definition
ROS_DB_PATH = os.getenv("ROS_DB_PATH")
MAP_DIR = ROS_DB_PATH + "/map"

# Source location for botcore
ROS_PACK = rospkg.RosPack()
CORE_PATH = os.path.join(ROS_PACK.get_path("bot_bringup"), "core_launch/")
DEVICE_PATH = os.path.join(ROS_PACK.get_path("bot_parameters"), "robot_setting.yaml")

ROBOT_ON = CORE_PATH + "roboton.launch.xml"
NAVIGATION = CORE_PATH + "nav.launch.xml"
SLAM = CORE_PATH + "slam.launch.xml"


def check_path():
	if not os.path.exists(MAP_DIR):
		os.makedirs(MAP_DIR)


class BotCore():
	def __init__(self):
		# Parameters
		self.is_exit_thread = False
		self.mode = "NAV"

		# Publisher
		self.pubs = {}
		self.pubs["MODE"] = rospy.Publisher("~MODE", String, queue_size=1)

		# Subscriber
		self.subs = []
		self.subs.append(rospy.Subscriber("bot_mode", String, self.bot_mode))

		# Service
		self.srvs = []
		self.srvs.append(rospy.Service("save_map", SaveMap, self.save_map))


	def __del__(self):
		for pub in self.pubs.values(): pub.unregister()
		for sub in self.subs: sub.unregister()
		for srv in self.srvs: srv.unregister()
		rospy.loginfo("Bot Core is shutdowned")


	def set_model(self):
		with open(DEVICE_PATH) as f:
			spec = yaml.safe_load(f)

		param_list = ["footprint"]

		for arg, value in spec.items():
			if arg in param_list and value != '':
				if arg == "footprint":
					polygon = value.split(',')
					footprint = "[[%s,%s],[%s,%s],[%s,%s],[%s,%s]]"%(polygon[0],polygon[2],polygon[1],polygon[2],polygon[1],polygon[3],polygon[0],polygon[3])
					os.environ["footprint"] = footprint

				rospy.set_param(arg, value)
			else:
				os.environ[arg] = value
			rospy.logwarn("[botcore] Set Param [%s] = %s"%(arg, value))


	def bot_mode(self, msg):
		if msg.data in ["INIT", "NAV", "SLAM", "RESET"]:
			rospy.loginfo("Robot starts with %s mode"%msg.data)
			self.mode = msg.data
		else:
			rospy.logwarn("Robot has got wrong type of mode")


	def call_savemap(self, filename, include_unfinished_submaps):
		""" save map for cartographer """
		srv_name = "write_state"
		try:
			rospy.wait_for_service(srv_name, timeout=0.5)
			srvs = rospy.ServiceProxy(srv_name, WriteState)
			resp = srvs.call(filename, include_unfinished_submaps)
			return resp.status.code
		except rospy.ServiceException as e:
			rospy.logerr("[botcore] Service call failed (call_savemap): %s"%e); return -1
		except rospy.ROSException as e:
			rospy.logerr("[botcore] TimeOut (call_savemap): %s"%e); return -1


	def save_map(self, req):
		if self.mode != "SLAM":
			return SaveMapResponse(False, "save_map is only available in SLAM mode", '', '')

		if not os.path.exists(MAP_DIR):
			os.mkdir(MAP_DIR)

		# Save Cartographer pbstream
		fname = "%s/map.pbstream"%MAP_DIR
		sm_status = self.call_savemap(fname, False)
		if sm_status != 0:
			message = "[botcore] SaveMap call is Fault!: %d"%sm_status
			rospy.logerr(message)
			return SaveMapResponse(False, message, '', '')

		# Save occupancy grid (.pgm + .yaml) via map_server
		subprocess.Popen('rosrun map_server map_saver --occ 50 --free 40 -f %s/map'%MAP_DIR, shell=True)

		return SaveMapResponse(True, "Save map call is succeeded", '', '')


	######################################################
	# Main Routines ######################################
	######################################################
	def botcore_start(self):
		# Get uuid from ros configure
		uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
		roslaunch.configure_logging(uuid)

		# INIT Mode launch
		eco_launch = roslaunch.parent.ROSLaunchParent(uuid, [ROBOT_ON])
		eco_launch.start()

		# Signal handler for is_exit_thread
		signal.signal(signal.SIGINT, self.sigint_handler)

		# Main Routine Start
		self.mode = "NAV"

		while not rospy.is_shutdown():
			if self.is_exit_thread:
				break

			if self.mode == "INIT":
				rospy.loginfo("INIT-Mode is on")
				self.routine_spin()

			elif self.mode == "NAV":
				launch = roslaunch.parent.ROSLaunchParent(uuid, [NAVIGATION])
				launch.start()
				rospy.loginfo("NAV-Mode is on")
				rospy.sleep(1)
				self.routine_spin()
				launch.shutdown()
				rospy.sleep(0.5)

			elif self.mode == "SLAM":
				launch = roslaunch.parent.ROSLaunchParent(uuid, [SLAM])
				launch.start()
				rospy.loginfo("SLAM-Mode is on")
				self.routine_spin()
				launch.shutdown()
				rospy.sleep(0.5)

			elif self.mode == "RESET":
				rospy.loginfo("Robot system is rebooted")
				eco_launch.shutdown()
				rospy.sleep(0.5)
				rospy.logwarn("ROS service restart")
				os.system("sudo service bot restart")
				self.is_exit_thread = True

			else:
				rospy.logerr("Something is wrong. The Bot Core will be shutdowned soon.")
				break

		eco_launch.shutdown()
		rospy.sleep(0.5)


	def routine_spin(self):
		now_mode = self.mode
		while now_mode == self.mode:
			rospy.sleep(1)
			self.pubs["MODE"].publish(self.mode)
			if self.is_exit_thread:
				break


	def sigint_handler(self, signum, frame):
		self.is_exit_thread = True


if __name__ == "__main__":
	rospy.init_node('bot_core')
	check_path()
	botcore = BotCore()
	botcore.set_model()
	botcore.botcore_start()
	rospy.spin()
