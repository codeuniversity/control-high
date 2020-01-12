from hlc.planner import planner
from hlc.planner.planner import plan
from hlc.planner.helper import Pose, HLAction
from hlc.tests.helper import generate_grid, navigate_grid


def test_empty_map_6x6():

    start_pose = Pose(0, 0, 0)
    test_pose = start_pose.copy()

    grid = generate_grid(grid_width, grid_height)
    plan_output = plan(grid_width, grid_height, start_pose)

    grid[start_pose.get_position()] = True
    navigate_grid(plan_output, grid, test_pose)

    # for a map without obstacles the robot needs to visit all positions
    for value in grid.values():
        assert value == True


def test_empty_map_4x5():
    grid_width, grid_height = (9, 7)

    start_pos = Pose(0, 0, 0)
    pos = start_pos.copy()

    grid = generate_grid(grid_width, grid_height)
    plan_output = plan(grid_width, grid_height, start_pos)

    grid[start_pos.get_position()] = True
    navigate_grid(plan_output, grid, pos)

    # for a map without obstacles the robot needs to visit all positions
    for value in grid.values():
        assert value == True


def test_one_obstacle_6x6():
    keys_grid = []
    start_pos = (0, 0)
    pos = (0, 0)
    grid_width, grid_height = (6, 6)
    obstacles = [(1, 2)]

    # create the grid as a dictionary
    # blocked - False, unexplored - None, explored - True
    for x in range(grid_dimension[1] + 1):
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
    navigate_grid(plan_output, grid)

    for action in plan_output:
        if action == HLAction.TURN_RIGHT:
            orientation = HLAction.right_turn(orientation)
            grid[pos] = True
        elif action == constants.MOVE_FORWARD:
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
        if action == constants.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos] = True
        elif action == constants.MOVE_FORWARD:
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
        if action == constants.TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[pos] = True
        elif action == constants.MOVE_FORWARD:
            pos = planner.add_pos_tuple(pos, orientation.value)
            grid[pos] = True

    for key, value in grid.items():
        # pos with obstacle, value needs to be false = pos not visited
        if key in obstacles:
            assert value != True
        else:  # all other pos must be visited
            assert value == True
