#Author: YuLong Pei, Zizhou Zhai
#!/usr/bin/env python

#robot.py implementation goes here

import rospy
from read_config import read_config
from std_msgs.msg import Bool
from cse_190_assi_3.msg import PolicyList
from cse_190_assi_3.msg import AStarPath
from astar import *
from mdp import *



class Robot():
	def publish_values(self,a):

		mdp_policyList = PolicyList()
		mdp_policyList.data = a;
		self.mdp_result_publisher.publish(mdp_policyList);

	def __init__(self):
		rospy.init_node("robot")
		
		# Read data from config file
		self.config = read_config()
		self.move_list = self.config["move_list"]
		self.walls = self.config["walls"]
		self.pits = self.config["pits"]
		
		# Set up publishers for robot
		self.AStar_result_publisher = rospy.Publisher(
			"/results/path_list",
			AStarPath,
			queue_size = 10
		)
		
		self.mdp_result_publisher = rospy.Publisher(
			"/results/policy_list",
			PolicyList,
			queue_size = 10
		)
		
		self.complete_sim = rospy.Publisher(
				"/map_node/sim_complete",
				Bool,
				queue_size = 10
		)
		
		rospy.sleep(1)
		A_path = APath()
		for x in A_path:
			a_path = AStarPath()
			a_path.data = x
			
			self.AStar_result_publisher.publish(a_path)

		MDP_calculation(self.publish_values)
		#MDP_calculation()

		b = Bool()
		b.data = True

		self.complete_sim.publish(b)

		rospy.signal_shutdown("Simulation complete")



if __name__ == '__main__':
	r = Robot()
