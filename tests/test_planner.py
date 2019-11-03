import numpy as np
import sys
sys.path.append('..')
from controlHigh.planner import plan, add_pos_tuple

def test_empty_map_6x6():
  keys = []
  pos = (0,0)


  for i in range(6):
    for j in range (6):
      keys = keys.append((i,j))
  all_positions = dict.fromkeys(keys, False)
  all_positions[(0,0)] = True
  plan_output = plan((6,6),np.array([]), np.array([]), (0,0))


  for action in plan_output:
    pos = add_pos_tuple(pos, action)
    all_positions[pos] = True

  for key, value in all_positions.items():
    assert value == True

def test_one_obsticle():
