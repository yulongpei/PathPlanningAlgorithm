# astar implementation needs to go here
from read_config import read_config
from util import print_2d_floats
from copy import deepcopy
import Queue

config = read_config()
row = config["map_size"][0]
col = config["map_size"][1]
orig_map = [[1 for x in range(col)]for x in range(row)]
for x in config["walls"]:
	orig_map[x[0]][x[1]] = 0
for x in config["pits"]:
	orig_map[x[0]][x[1]] = 0
moves = config["move_list"]

def APath():
	h_map = heuristics()
	ucost_map = [[0 for x in range(col)]for x in range(row)]
	visited = []
	q = Queue.PriorityQueue()
	prev = {}

	q.put(config["start"],0);
	while not q.empty():
		cur_stage = q.get()
		visited.append(cur_stage)
		if [cur_stage[0],cur_stage[1]] == config["goal"]:
			continue;

		for x in moves:
			posy = cur_stage[0]+x[0]
			posx = cur_stage[1]+x[1]
			if posx < 0 or posx >= col:
				continue
			if posy < 0 or posy >= row:
				continue
			if orig_map[posy][posx] == 0:
				continue
			tentativeCost = ucost_map[cur_stage[0]][cur_stage[1]] + 1
			if tentativeCost < ucost_map[posy][posx] or ucost_map[posy][posx] == 0:
				ucost_map[posy][posx] = tentativeCost
				q.put([posy,posx],tentativeCost + h_map[posy][posx])
				prev[(posy,posx)] = (cur_stage[0],cur_stage[1])

	backward_path = []
	prev_stage = config["goal"]
	while prev_stage != config["start"]:
		backward_path.append(prev_stage)
		prev_stage = [prev[(prev_stage[0],prev_stage[1])][0],prev[(prev_stage[0],prev_stage[1])][1]]
	backward_path.append(prev_stage)

	backward_path.reverse()
	#print backward_path
	return backward_path


def heuristics():
	h_map = [[0 for x in range(col)]for x in range(row)]
	visited = []
	q = Queue.Queue()

	q.put(config["goal"]);
	while not q.empty():
		cur_stage = q.get()
		visited.append(cur_stage)
		for x in moves:
			posy = cur_stage[0]+x[0]
			posx = cur_stage[1]+x[1]
			if posx < 0 or posx >= col:
				continue
			if posy < 0 or posy >= row:
				continue
			if [posy,posx] in visited:
				continue
			q.put([posy,posx])
			h_map[posy][posx] = h_map[cur_stage[0]][cur_stage[1]]+1

	return h_map
