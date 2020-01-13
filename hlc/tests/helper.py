from hlc.config.constants import *
from hlc.planner.helper import Pose, HLAction
from hlc.planner.planner import plan, Map2D
from typing import List, Tuple

from multiprocessing import Process, Queue

Position = Tuple[int, int]


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


def navigate_grid(plan: List[HLAction], grid: Map2D, position: Pose):

    for action in plan:
        position.update(action)
        grid[position.get_position()] = True


def process_wrapper(function, args, result_queue):
    result = function(*args)
    result_queue.put(result)


def generate_plan_with_timeout(timeout, plan_args):
    result_queue = Queue()
    planing_process = Process(target=process_wrapper,
                              args=(plan, plan_args, result_queue))
    planing_process.start()
    planing_process.join(timeout)

    if planing_process.is_alive():
        planing_process.terminate()
        raise TimeoutError("The Planning function took too long to finish")
    return result_queue.get()


def create_solution_grid(grid_width: int, grid_height: int, start_pose: Pose, obstacle_positions=[]):
    grid = Map2D(grid_width, grid_height, obstacle_positions)
    grid[start_pose.get_position()] = True

    plan_output = generate_plan_with_timeout(
        2, (grid_width, grid_height, start_pose.copy()))
    navigate_grid(plan_output, grid, start_pose)

    return grid


def check_solution_grid(grid: Map2D, obstacles: List[Position]):
    for position in grid.obstacle_grid:
        if position in obstacles:
            assert grid[position] == False
        else:
            assert grid[position] == True
