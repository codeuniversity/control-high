import numpy as np
import sys
sys.path.append('..')
from hlc.planner import plan, add_pos_tuple

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
  for key, value in all_positions.items():
    if key == (1,2): # pos with obsticle, value needs to be false = pos not visited
      assert value != True
    else: # all other pos must be visited
      assert value == True


def test_multiple_obsticle_6x6():
  keys = []
  pos = (0,0)

  #create all keys aka all position in the grid
  for i in range(6):
    for j in range (6):
      keys.append((i,j))

  # create dic with all possible position, set value to False = pos not visited
  all_positions = dict.fromkeys(keys, False)
  all_positions[(0,0)] = True

  plan_output = plan((6,6),np.array([[0,2], [1,5], [3,4], [5,2]]), np.array([]), (0,0))

  # if position visited change value to True
  for action in plan_output:
    pos = add_pos_tuple(pos, action)
    all_positions[pos] = True

  # pos_blocked needs to be False, all other pos True --> robot explored the whole map with multiple obstacles
  for key, value in all_positions.items():
    if key == (0,2): # pos with obsticle, value needs to be False = pos not visited
      assert value != True
    elif key == (1,5):
      assert value != True
    elif key == (3,4):
      assert value != True
    elif key == (5,2):
      assert value != True
    else: # all other pos must be visited
      assert value == True


def test_dead_end_6x6():
  keys = []
  pos = (0,0)

  #create all keys aka all position in the grid
  for i in range(6):
    for j in range (6):
      keys.append((i,j))

  # create dic with all possible position, set value to False = pos not visited
  all_positions = dict.fromkeys(keys, False)
  all_positions[(0,0)] = True

  # only open pos at [2,0], robot still needs to explore all (0,x) and (1,x) and then walk backwards to explore rest of map
  plan_output = plan((6,6),np.array([[2,1], [2,2], [2,3], [2,4], [2,5]]), np.array([]), (0,0))

  # if position visited change value to True
  for action in plan_output:
    pos = add_pos_tuple(pos, action)
    all_positions[pos] = True

  # pos_blocked needs to be False, all other pos True --> robot explored the whole map with one dead end
  for key, value in all_positions.items():
    if key == (1,1): # pos with obsticle, value needs to be false = pos not visited
      assert value != True
    elif key == (1,2):
      assert value != True
    elif key == (1,3):
      assert value != True
    elif key == (1,4):
      assert value != True
    elif key == (1,5):
      assert value != True
    else: # all other pos must be visited
      assert value == True



# missing: start position (0,0) is blocked --> new start position or executor panic & replanning?
