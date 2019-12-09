from hlc.config.constants import *
from hlc.planner.helper import Pose, HLAction


def right_turn(orientation):
    if orientation == FORWARD:
        orientation = RIGHT
    elif orientation == RIGHT:
        orientation = BACKWARD
    elif orientation == BACKWARD:
        orientation = LEFT
    elif orientation == LEFT:
        orientation = FORWARD

    return orientation


def generate_grid(grid_dimension, obstacles=[]):
    keys_grid = []

    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))

    grid = dict.fromkeys(keys_grid, None)
    for o in obstacles:
        grid[o] = False
    return grid


def navigate_grid(plan, grid, position):

    for action in plan:
        position.update(action)
        grid[position.get_position()] = True
