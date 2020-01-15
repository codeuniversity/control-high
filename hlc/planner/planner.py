# from hlc.config.constants import *
from hlc.planner.helper import Pose, HLAction
from typing import Tuple, List
from math import sqrt

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
        for i in range(1, len(self.corners) - 1):
            self.corners[i].previous_corner = self.corners[i-1]
            self.corners[i].next_corner = self.corners[i+1]

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

    max_layer_index = min(grid_height, grid_width) // 2

    while layer_map.layer_index < max_layer_index:

        layer = layer_map.generate_rectangle_layer()

        actions = progress_through_layer(
            layer, robot_pose, final_layer_position)
        plan.extend(actions)

        switch_layer_actions = [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD]
        apply_actions(switch_layer_actions, robot_pose, plan)
        final_layer_position = get_new_final_layer_position(robot_pose)
        layer_map.switchLayer(layer_map.layer_index + 1)

    if grid_width != grid_height and layer_map.layer_index == max_layer_index:
        if grid_width % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
            while robot_pose.position[0] < grid_width - layer_map.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)
        else:
            while robot_pose.position[1] < grid_height - layer_map.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

    return plan


def get_new_final_layer_position(robot_pose: Pose) -> Position:
    return robot_pose.copy().add_position((1, 0))


def progress_through_layer(layer: Layer, robot_pose: Pose, final_layer_position: Position) -> List[HLAction]:
    progress = []
    while robot_pose.get_position() != final_layer_position:
        apply_actions([HLAction.MOVE_FORWARD], robot_pose, progress)

        if layer.corners[1].position == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)
        elif layer.corners[2].position == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)
        elif layer.corners[3].position == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)

    return progress
