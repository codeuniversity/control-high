from enum import Enum

class Action(Enum):
  FORWARD = (0,1)
  RIGHT_FORWARD = (1,1)
  RIGHT = (1,0)
  RIGHT_BACKWARD = (1,-1)
  BACKWARD = (0,-1)
  LEFT_BACKWARD = (-1,-1)
  LEFT = (-1,0)
  LEFT_FORWARD = (-1,1)

def add_pos_tuple(t1, t2):
  new_x = t1[0] + t2[0]
  new_y = t1[1] + t2[1]
  return (new_x, new_y)

def plan(map_dim, edges_blocked, edges_free, current_pos):
  return []
