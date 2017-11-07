# mdp implementation needs to go here
from copy import deepcopy
from read_config import read_config

config = read_config()
row = config["map_size"][0]
col = config["map_size"][1]
orig_map = [[1 for x in range(col)]for x in range(row)]
for x in config["walls"]:
	orig_map[x[0]][x[1]] = 0
for x in config["pits"]:
	orig_map[x[0]][x[1]] = -1
moves = config["move_list"]

value_map = [[0.0 for x in range(col)]for x in range(row)]
value_map[config["goal"][0]][config["goal"][1]] = config["reward_for_reaching_goal"]
for x in config["pits"]:
	value_map[x[0]][x[1]] = config["reward_for_falling_in_pit"]

direction_map = [["" for x in range(col)]for x in range(row)]
for x in config["walls"]:
	direction_map[x[0]][x[1]] = "WALL"
for x in config["pits"]:
	direction_map[x[0]][x[1]] = "PIT"
direction_map[config["goal"][0]][config["goal"][1]] = "GOAL"



def MDP_calculation(callback):
	global value_map
	iterations = 0
	while iterations < config["max_iterations"]:
		#loop through all cells
		new_value_map = deepcopy(value_map)
		for y in range(row):
			for x in range(col):

				#check if the cell is open space
				if orig_map[y][x] == 1:
					if y == config["goal"][0] and x == config["goal"][1]:
						continue

					#loop through the moves and save all value returned to find max
					direction_value = []
					value_only = []
					for move in moves:
						curr_value = step_value_calculation(y,x,move)
						direction_value.append((move,curr_value))
						value_only.append(curr_value)

					max_value = max(value_only)
		

					#find the move that correspond to the max value
					max_move = []
					for direct in direction_value:
						if max_value == direct[1]:
							max_move = direct[0]
							break;
					new_value_map[y][x] = max_value

					#update the direction map
					if max_move[0] == 0:
						if max_move[1] == 1:
							direction_map[y][x] = "E"
						else:
							direction_map[y][x] = "W"
					else:
						if max_move[0] == 1:
							direction_map[y][x] = "S"
						else:
							direction_map[y][x] = "N"
		
		diff = calculate_sum_absolute_diff(value_map,new_value_map)
		value_map = deepcopy(new_value_map)



		policy_list = []
		for x in direction_map:
			for y in x:
				policy_list.append(y)
		
		callback(policy_list)

		if diff < config["threshold_difference"]:
			break;
		iterations = iterations + 1




def calculate_sum_absolute_diff(a, b):

	diff_sum = 0;
	for y in range(row):
		for x in range(col):
			diff_sum += abs(a[y][x] - b[y][x])

	return diff_sum;

def step_value_calculation(rowy,colx,move):

	value_sum = 0.0;

	# move forward value.
	new_rowy = rowy+move[0]
	new_colx = colx+move[1]

	if new_rowy >= row or new_colx >= col or new_rowy < 0 or new_colx < 0 or orig_map[new_rowy][new_colx] == 0:
		#if hit wall
		value_sum += config["prob_move_forward"]*(config["reward_for_hitting_wall"]+config["discount_factor"]*value_map[rowy][colx])
	elif orig_map[new_rowy][new_colx] == -1:
		#if hit pit
		value_sum += config["prob_move_forward"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])
	else:
		#moved correctly
		value_sum += config["prob_move_forward"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])

	# move backwards
	new_rowy = rowy+(move[0]* -1)
	new_colx = colx+(move[1]* -1)

	if new_rowy >= row or new_colx >= col or new_rowy < 0 or new_colx < 0 or orig_map[new_rowy][new_colx] == 0:
		#if hit wall
		value_sum += config["prob_move_backward"]*(config["reward_for_hitting_wall"]+config["discount_factor"]*value_map[rowy][colx] )
	elif orig_map[new_rowy][new_colx] == -1:
		#if hit pit
		value_sum += config["prob_move_backward"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])
	else:
		#moved correctly
		value_sum += config["prob_move_backward"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])

	# move left
	# find left
	if move[0] == -1 and move[1] == 0:
		new_rowy_delta = 0
		new_colx_delta = -1
	elif move[0] == 0 and move[1] == -1:
		new_rowy_delta = 1
		new_colx_delta = 0
	elif move[0] == 1 and move[1] == 0:
		new_rowy_delta = 0
		new_colx_delta = 1
	else:
		new_rowy_delta = -1
		new_colx_delta = 0

	new_rowy = rowy+new_rowy_delta
	new_colx = colx + new_colx_delta;

	if new_rowy >= row or new_colx >= col or new_rowy < 0 or new_colx < 0 or orig_map[new_rowy][new_colx] == 0:
		#if hit wall
		value_sum += config["prob_move_left"]*(config["reward_for_hitting_wall"] +config["discount_factor"]*value_map[rowy][colx])
	elif orig_map[new_rowy][new_colx] == -1:
		#if hit pit
		value_sum += config["prob_move_left"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])
	else:
		#moved correctly
		value_sum += config["prob_move_left"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])

	# move right
	new_rowy = rowy +(new_rowy_delta)* -1
	new_colx = colx + (new_colx_delta)* -1

	if new_rowy >= row or new_colx >= col or new_rowy < 0 or new_colx < 0 or orig_map[new_rowy][new_colx] == 0:
		#if hit wall
		value_sum += config["prob_move_right"]*(config["reward_for_hitting_wall"] +config["discount_factor"]*value_map[rowy][colx])
	elif orig_map[new_rowy][new_colx] == -1:
		#if hit pit
		value_sum += config["prob_move_right"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])
	else:
		#moved correctly
		value_sum += config["prob_move_right"]*(config["reward_for_each_step"] + config["discount_factor"]*value_map[new_rowy][new_colx])


	return value_sum;

