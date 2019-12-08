from hlc.plan import planner
from enum import Enum
import numpy as np


class Orientation(Enum):
    FORWARD = (0, 1)
    RIGHT = (1, 0)
    BACKWARD = (0, -1)
    LEFT = (-1, 0)


def right_turn(orientation):
    if orientation.name == "FORWARD":
        orientation = Orientation.RIGHT
    elif orientation.name == "RIGHT":
        orientation = Orientation.BACKWARD
    elif orientation.name == "BACKWARD":
        orientation = Orientation.LEFT
    elif orientation.name == "LEFT":
        orientation = Orientation.FORWARD

    return orientation


def test_empty_map_6x6():
    keys_grid = []
    start_pos = (0, 0)
    pos = planner.Position(start_pos)
    grid_dimension = (6, 6)

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid_dimension, start_pos)

    # execute the actions and set explored pos to True
    orientation = Orientation.FORWARD
    for action in plan_output:
        if action == planner.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos.current()] = True
        elif action == planner.MOVE_FORWARD:
            pos.update(orientation.value)
            grid[pos.current()] = True

    # for a map without obstacles the robot needs to visit all positions
    for value in grid.values():
        assert value == True


def test_empty_map_4x5():
    keys_grid = []
    start_pos = (0, 0)
    pos = planner.Position(start_pos)
    grid_dimension = (4, 5)

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid_dimension, start_pos)

    # execute the actions and set explored pos to True
    orientation = Orientation.FORWARD
    for action in plan_output:
        if action == planner.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos.current()] = True
        elif action == planner.MOVE_FORWARD:
            pos.update(orientation.value)
            grid[pos.current()] = True

    # for a map without obstacles the robot needs to visit all positions
    for value in grid.values():
        assert value == True


def test_one_obstacle_6x6():
    keys_grid = []
    start_pos = (0, 0)
    pos = (0, 0)
    grid_dimension = (6, 6)
    obstacles = [(1, 2)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid_dimension, start_pos)

    # execute the actions and set explored pos to True
    for action in plan_output:
        if action == planner.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos] = True
        elif action == planner.MOVE_FORWARD:
            pos = planner.add_pos_tuple(pos, orientation.value)
            grid[pos] = True

    for key, value in grid.items():
        # pos with obstacle, value needs to be false = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True


def test_multiple_obstacle_6x6():
    keys_grid = []
    start_pos = (0, 0)
    pos = (0, 0)
    grid_dimension = (6, 6)
    obstacles = [(2, 1), (3, 4), (5, 1), (5, 4)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid_dimension, (0, 0))

    # execute the actions and set explored pos to True
    for action in plan_output:
        if action == planner.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos] = True
        elif action == planner.MOVE_FORWARD:
            pos = planner.add_pos_tuple(pos, orientation.value)
            grid[pos] = True

    for key, value in grid.items():
        # pos with obstacle, value needs to be False = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True


def test_dead_end_6x6():
    keys_grid = []
    start_pos = (0, 0)
    pos = (0, 0)
    grid_dimension = (6, 6)
    obstacles = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))

    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid_dimension, (0, 0))

    # execute the actions and set explored pos to True
    for action in plan_output:
        if action == planner.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos] = True
        elif action == planner.MOVE_FORWARD:
            pos = planner.add_pos_tuple(pos, orientation.value)
            grid[pos] = True

    for key, value in grid.items():
        # pos with obstacle, value needs to be false = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True
