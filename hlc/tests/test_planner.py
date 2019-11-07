from hlc.plan import planner
import numpy as np


def test_empty_map_6x6():
    keys_grid = []
    start_pos = (0, 0)

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(6):
        for y in range(6):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid, start_pos)

    # execute the actions and set explored pos to True
    for action in plan_output:
        pos = planner.add_pos_tuple(pos, action)
        grid[pos] = True

    # for a map without obstacles the robot needs to visit all positions
    for value in grid.values():
        assert value == True


def test_one_obstacle_6x6():
    keys_grid = []
    start_pos = (0, 0)
    obstacles = [(1,2)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(6):
        for y in range(6):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid, start_pos)

    # execute the actions and set explored pos to True
    for action in plan_output:
        pos = planner.add_pos_tuple(pos, action)
        grid[pos] = True

    for key, value in grid.items():
        # pos with obsticle, value needs to be false = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True


def test_multiple_obsticle_6x6():
    keys_grid = []
    start_pos = (0, 0)
    obstacles = [(2, 1), (3, 4), (5, 1), (5, 4)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(6):
        for y in range(6):
            keys_grid.append((x, y))
    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid, (0, 0))

    # execute the actions and set explored pos to True
    for action in plan_output:
        pos = planner.add_pos_tuple(pos, action)
        grid[pos] = True

    for key, value in grid.items():
        # pos with obsticle, value needs to be False = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True


def test_dead_end_6x6():
    keys_grid = []
    start_pos = (0, 0)
    obstacles = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(6):
        for y in range(6):
            keys_grid.append((x, y))

    grid = dict.fromkeys(keys_grid, None)

    # set obstacle position to False
    for key in grid:
        if key in obstacles:
            grid[key] = False

    # set start position to explored
    grid[start_pos] = True

    plan_output = planner.plan(grid, (0, 0))

    # execute the actions and set explored pos to True
    for action in plan_output:
        pos = planner.add_pos_tuple(pos, action)
        grid[pos] = True

    for key, value in grid.items():
        # pos with obsticle, value needs to be false = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True
