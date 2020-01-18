from hlc.planner.helper import Vector, Pose, HLAction
from hlc.planner.maps import Layered2DMap, Layer
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal


def generate_plan(target_map: Layered2DMap, start_pose=Pose(0, 0, 0)) -> List[HLAction]:
    robot = Agent(start_pose)

    max_layer_index = min(target_map.width, target_map.height) / 2

    plan = []
    while target_map.layer_index < max_layer_index:

        layer = target_map.generate_rectangle_layer()

        actions = robot.progress_through_layer(layer)
        plan.extend(actions)

        target_map.switchLayer(target_map.layer_index + 1)

    return plan


class Agent():
    def __init__(self, start_pose: Pose):
        self.pose = start_pose

    def progress_through_layer(self, rectangle_layer: Layer) -> List[HLAction]:
        progress = []
        current_corner = rectangle_layer.get_closest_corner(self.pose.position)
        for _ in range(len(rectangle_layer.corners) + 1):
            actions = self.move_to(current_corner.position)
            progress.extend(actions)
            current_corner = current_corner.next_corner
        return progress

    def move_to(self, position: Vector) -> List[HLAction]:
        x_difference = int(position.get_x() - self.pose.position.get_x())
        y_difference = int(position.get_y() - self.pose.position.get_y())

        actions = []

        if x_difference != 0:
            actions.extend(
                self.align_orientation(Vector(x_difference, 0))
            )

            for _ in range(abs(x_difference)):
                a = HLAction.MOVE_FORWARD
                self.pose.apply_action(a)
                actions.append(a)

        if y_difference != 0:
            actions.extend(
                self.align_orientation(Vector(0, y_difference))
            )

            for _ in range(abs(y_difference)):
                a = HLAction.MOVE_FORWARD
                self.pose.apply_action(a)
                actions.append(a)

        return actions

    def align_orientation(self, vector: Vector):
        y_axis = self.pose.orientation
        x_axis = self.pose.orientation.rotate(90)

        angle_y_axis = vector.get_angle_to(y_axis)
        angle_x_axis = vector.get_angle_to(x_axis)
        if angle_x_axis <= 90:
            rotation_direction = 1
        else:
            rotation_direction = -1

        actions = []
        for _ in range(0, int(angle_y_axis), 90):
            a = HLAction((0, 0, rotation_direction * 90))
            self.pose.apply_action(a)
            actions.append(a)

        return actions
