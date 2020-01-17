# from hlc.config.constants import *
from hlc.planner.helper import Pose, HLAction
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal

Position = Tuple[int, int]


class Map2D():
    def __init__(self, width: int, height: int, obstacle_positions: List[Position]):
        self.width = width
        self.height = height
        self.obstacle_grid = self._generate_grid(obstacle_positions)

    def _generate_grid(self, obstacles_positions: List[Position]):
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

    def __init__(self, width: int, height: int, obstacle_positions: List[Position], layer_index=0):
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
            (min_width, min_height),
            (min_width, max_height),
            (max_width, max_height),
            (max_width, min_height)
        ]
        return Layer(corner_positions)


class Corner():
    def __init__(self, position: Position):
        self.position = position
        self.next_corner: Corner
        self.previous_corner: Corner


class Layer():
    def __init__(self, corner_positions: List[Position]):
        self.corners = []

        for position in corner_positions:
            self.corners.append(Corner(position))

        self.corners[0].previous_corner = self.corners[-1]
        self.corners[-1].next_corner = self.corners[0]
        for i in range(len(self.corners) - 1):
            self.corners[i].next_corner = self.corners[i+1]
        for i in range(1, len(self.corners)):
            self.corners[i].previous_corner = self.corners[i-1]

    def get_closest_corner(self, position: Position) -> Corner:
        min_distance = float("inf")
        closest_corner = None
        for c in self.corners:
            distance = get_distance(c.position, position)
            if distance < min_distance:
                closest_corner = c
                min_distance = distance
        return closest_corner


def get_distance(point1: Position, point2: Position):
    x_difference = point1[0] - point2[0]
    y_difference = point1[1] - point2[1]
    total_distance = sqrt(x_difference**2 + y_difference**2)
    return total_distance


def apply_actions(actions: List[HLAction], robot_pose: Pose, plan: List[HLAction]):
    for a in actions:
        plan.append(a)
        robot_pose.apply_action(a)


def update_position(pose: Pose, new_actions: List[HLAction]):
    for action in new_actions:
        pose.apply_action(action)


def plan(grid_width: int, grid_height: int, start_pose=Pose(0, 0, 0), layer_index=0) -> List[HLAction]:
    robot_pose = start_pose.copy()
    plan = []
    final_layer_position = get_new_final_layer_position(robot_pose)

    layer_map = Layered2DMap(grid_width, grid_height, [], layer_index)

    max_layer_index = min(grid_height, grid_width) / 2

    while layer_map.layer_index < max_layer_index:

        layer = layer_map.generate_rectangle_layer()

        actions = progress_through_layer(
            layer, robot_pose, final_layer_position)
        plan.extend(actions)

        layer_map.switchLayer(layer_map.layer_index + 1)

    return plan


def get_angle_between_vectors(vector1: np.ndarray, vector2: np.ndarray):
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    cos_angle = np.dot(vector1, vector2) / (norm_vector1 * norm_vector2)
    return round(degrees(acos(cos_angle)), 5)


def normalize_vector(vector: np.ndarray):
    vector_norm = np.linalg.norm(vector)
    return vector / vector_norm


def get_new_final_layer_position(robot_pose: Pose) -> Position:
    return robot_pose.copy().add_position((1, 0))


def align_orientation(vector, robot_pose):
    y_axis = robot_pose.orientation
    x_axis = robot_pose.rotate_vector(robot_pose.orientation, 90)

    angle_y_axis = get_angle_between_vectors(vector, np.array(y_axis))
    angle_x_axis = get_angle_between_vectors(vector, np.array(x_axis))
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


def move_to(position: Position, robot_pose: Pose) -> List[HLAction]:
    x_difference = int(position[0] - robot_pose.position[0])
    y_difference = int(position[1] - robot_pose.position[1])

    actions = []

    if x_difference != 0:
        actions.extend(
            align_orientation(np.array((x_difference, 0)), robot_pose)
        )

        for _ in range(abs(x_difference)):
            a = HLAction.MOVE_FORWARD
            robot_pose.apply_action(a)
            actions.append(a)

    if y_difference != 0:
        actions.extend(
            align_orientation(np.array((0, y_difference)), robot_pose)
        )

        for _ in range(abs(y_difference)):
            a = HLAction.MOVE_FORWARD
            robot_pose.apply_action(a)
            actions.append(a)

    return actions


def progress_through_layer(layer: Layer, robot_pose: Pose, final_layer_position: Position) -> List[HLAction]:
    progress = []
    current_corner = layer.get_closest_corner(robot_pose.position)
    for _ in range(len(layer.corners) + 1):
        actions = move_to(current_corner.position, robot_pose)
        progress.extend(actions)
        current_corner = current_corner.next_corner
    return progress
