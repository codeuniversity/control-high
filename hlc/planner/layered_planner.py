from hlc.planner.helper import Vector, Pose, HLAction
from hlc.planner.maps import Layered2DMap, Layer
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal


class LayeredPlanner():
    def __init__(self, target_map: Layered2DMap, start_pose: Pose):
        self.pose = start_pose.copy()
        self.target_map = target_map

    def generate_plan(self) -> List[HLAction]:
        max_layer_index = min(self.target_map.width,
                              self.target_map.height) / 2

        plan = []
        while self.target_map.layer_index < max_layer_index:

            layer = self.target_map.generate_rectangle_layer()

            actions = self.progress_through_layer(layer)
            plan.extend(actions)

            self.target_map.layer_index += 1
        return plan

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
