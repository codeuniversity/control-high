# from hlc.config.constants import *
from hlc.planner.helper import Vector, Pose, HLAction
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal


class Map2D():
    def __init__(self, width: int, height: int, obstacle_positions: List[Tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacle_grid = self._generate_grid(obstacle_positions)

    def _generate_grid(self, obstacles_positions: List[Tuple[int, int]]):
        keys_grid = []

        for x in range(self.width):
            for y in range(self.height):
                keys_grid.append((x, y))

        grid = dict.fromkeys(keys_grid, None)
        for o in obstacles_positions:
            grid[o] = False
        return grid

    def __getitem__(self, key):
        return self.obstacle_grid[key]

    def __setitem__(self, key, value):
        self.obstacle_grid[key] = value

    def obstacle_grid_values(self):
        return self.obstacle_grid.values()


class Layered2DMap(Map2D):

    def __init__(self, width: int, height: int, obstacle_positions: List[Vector], layer_index=0):
        super().__init__(width, height, obstacle_positions)
        self.layer_index = layer_index

    def switchLayer(self, layer_index: int):
        self.layer_index = layer_index

    def generate_rectangle_layer(self):
        min_width = self.layer_index
        min_height = self.layer_index
        max_width = self.width - self.layer_index - 1
        max_height = self.height - self.layer_index - 1

        corner_positions = [
            Vector(min_width, min_height),
            Vector(min_width, max_height),
            Vector(max_width, max_height),
            Vector(max_width, min_height)
        ]
        return Layer(corner_positions)


class Corner():
    def __init__(self, position: Vector):
        self.position = position
        self.next_corner: Corner
        self.previous_corner: Corner


class Layer():
    def __init__(self, corner_positions: List[Vector]):
        self.corners = []

        for position in corner_positions:
            self.corners.append(Corner(position))

        self.corners[0].previous_corner = self.corners[-1]
        self.corners[-1].next_corner = self.corners[0]
        for i in range(len(self.corners) - 1):
            self.corners[i].next_corner = self.corners[i+1]
        for i in range(1, len(self.corners)):
            self.corners[i].previous_corner = self.corners[i-1]

    def get_closest_corner(self, position: Vector) -> Corner:
        min_distance = float("inf")
        closest_corner = None
        for c in self.corners:
            distance = position.get_distance_to(c.position)
            if distance < min_distance:
                closest_corner = c
                min_distance = distance
        return closest_corner


def apply_actions(actions: List[HLAction], robot_pose: Pose, plan: List[HLAction]):
    for a in actions:
        plan.append(a)
        robot_pose.apply_action(a)


def plan(grid_width: int, grid_height: int, start_pose=Pose(0, 0, 0), layer_index=0) -> List[HLAction]:
    robot_pose = start_pose.copy()
    plan = []

    layer_map = Layered2DMap(grid_width, grid_height, [], layer_index)

    max_layer_index = min(grid_height, grid_width) / 2

    while layer_map.layer_index < max_layer_index:

        layer = layer_map.generate_rectangle_layer()

        actions = progress_through_layer(layer, robot_pose)
        plan.extend(actions)

        layer_map.switchLayer(layer_map.layer_index + 1)

    return plan


def align_orientation(vector: Vector, robot_pose: Pose):
    y_axis = robot_pose.orientation
    x_axis = robot_pose.orientation.rotate(90)

    angle_y_axis = vector.get_angle_to(y_axis)
    angle_x_axis = vector.get_angle_to(x_axis)
    if angle_x_axis <= 90:
        rotation_direction = 1
    else:
        rotation_direction = -1

    actions = []
    for _ in range(0, int(angle_y_axis), 90):
        a = HLAction((0, 0, rotation_direction * 90))
        robot_pose.apply_action(a)
        actions.append(a)

    return actions


def move_to(position: Vector, robot_pose: Pose) -> List[HLAction]:
    x_difference = int(position.get_x() - robot_pose.position.get_x())
    y_difference = int(position.get_y() - robot_pose.position.get_y())

    actions = []

    if x_difference != 0:
        actions.extend(
            align_orientation(Vector(x_difference, 0), robot_pose)
        )

        for _ in range(abs(x_difference)):
            a = HLAction.MOVE_FORWARD
            robot_pose.apply_action(a)
            actions.append(a)

    if y_difference != 0:
        actions.extend(
            align_orientation(Vector(0, y_difference), robot_pose)
        )

        for _ in range(abs(y_difference)):
            a = HLAction.MOVE_FORWARD
            robot_pose.apply_action(a)
            actions.append(a)

    return actions


def progress_through_layer(layer: Layer, robot_pose: Pose) -> List[HLAction]:
    progress = []
    current_corner = layer.get_closest_corner(robot_pose.position)
    for _ in range(len(layer.corners) + 1):
        actions = move_to(current_corner.position, robot_pose)
        progress.extend(actions)
        current_corner = current_corner.next_corner
    return progress
