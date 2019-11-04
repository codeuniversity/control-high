import numpy as np
import sys
sys.path.append('..')
from controlHigh.planner import plan, add_pos_tuple

def test_empty_map_6x6():
  keys = []
  pos = (0,0)

  #create all keys aka all position in the grid
  for i in range(6):
    for j in range (6):
      keys.append((i,j))

  # create dic with all possible position, set value to False = pos not visited
  all_positions = dict.fromkeys(keys, False)
  all_positions[(0,0)] = True
  plan_output = plan((6,6),np.array([]), np.array([]), (0,0))

  # if position visited change value to True
  for action in plan_output:
    pos = add_pos_tuple(pos, action)
    all_positions[pos] = True

  # for a map without obstacles the robot needs to visit all positions
  for value in all_positions.values():
    assert value == True


def test_one_obsticle_6x6():
  keys = []
  pos = (0,0)

  #create all keys aka all position in the grid
  for i in range(6):
    for j in range (6):
      keys.append((i,j))

  # create dic with all possible position, set value to False = pos not visited
  all_positions = dict.fromkeys(keys, False)
  all_positions[(0,0)] = True

  plan_output = plan((6,6),np.array([[1,2]]), np.array([]), (0,0))

  # if position visited change value to True
  for action in plan_output:
    pos = add_pos_tuple(pos, action)
    all_positions[pos] = True

  # pos_blocked needs to be False, all other pos True --> robot explored the whole map with one obstacle
  for keys, value in all_positions.items():
    if keys == (1,2): # pos with obsticle, value needs to be false = pos not visited
      assert value != True
    else: # all other pos must be visited
      assert value == True

