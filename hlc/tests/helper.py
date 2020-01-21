from hlc.planner.helper import Pose, HLAction
from hlc.planner import LayeredPlanner
from hlc.planner.maps import Map2D, Layered2DMap
from typing import List, Tuple

from multiprocessing import Process, Queue

Position = Tuple[int, int]


def navigate_grid(plan: List[HLAction], test_map: Map2D, pose: Pose):
    test_map.set_obstacle((pose.x, pose.y), True)
    for action in plan:
        pose.apply_action(action)
        test_map.set_obstacle((pose.x, pose.y), True)


def create_solution_grid(grid_width: int, grid_height: int, start_pose: Pose, obstacle_positions=[]) -> Layered2DMap:
    test_map = Layered2DMap(grid_width, grid_height, obstacle_positions)
    planner = LayeredPlanner(test_map, start_pose)
    plan = planner.generate_plan()

    navigate_grid(plan, test_map, start_pose)

    return test_map


def check_solution_grid(test_map: Map2D, obstacles: List[Position]):
    for position in test_map.obstacle_grid:
        if position in obstacles:
            assert test_map.get_obstacle(position) == False
        else:
            assert test_map.get_obstacle(position) == True
