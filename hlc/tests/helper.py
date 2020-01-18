from hlc.planner.helper import Pose, HLAction
from hlc.planner.planner import generate_plan
from hlc.planner.maps import Map2D, Layered2DMap
from typing import List, Tuple

from multiprocessing import Process, Queue

Position = Tuple[int, int]


def navigate_grid(plan: List[HLAction], grid: Map2D, position: Pose):

    for action in plan:
        position.apply_action(action)
        grid[position.get_position()] = True


def process_wrapper(function, args, result_queue):
    result = function(*args)
    result_queue.put(result)


def create_solution_grid(grid_width: int, grid_height: int, start_pose: Pose, obstacle_positions=[]):
    test_map = Layered2DMap(grid_width, grid_height, obstacle_positions)
    test_map[start_pose.get_position()] = True

    plan_output = generate_plan(test_map, start_pose.copy())
    navigate_grid(plan_output, test_map, start_pose)

    return test_map


def get_grid_value(grid: Map2D, position: Position):
    return grid[position]


def check_solution_grid(grid: Map2D, obstacles: List[Position]):
    for position in grid.obstacle_grid:
        if position in obstacles:
            assert get_grid_value(grid, position) == False
        else:
            assert get_grid_value(grid, position) == True
