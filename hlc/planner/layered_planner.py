from hlc.planner.helper import Vector, Pose, HLAction
from hlc.planner.maps import Layered2DMap, Layer
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal


class LayeredPlanner():
    def __init__(self, target_map: Layered2DMap, start_pose: Pose):
        self.__pose = start_pose.copy()
        self.__target_map = target_map

    def generate_plan(self) -> List[HLAction]:
        max_layer_index = min(self.__target_map.width,
                              self.__target_map.height) / 2

        plan = []
        while self.__target_map.layer_index < max_layer_index:

            layer = self.__target_map.generate_rectangle_layer()

            actions = self.progress_through_layer(layer)
            plan.extend(actions)

            self.__target_map.layer_index += 1
        return plan

    def progress_through_layer(self, rectangle_layer: Layer) -> List[HLAction]:
        progress = []
        current_corner = rectangle_layer.get_closest_corner(
            Vector(self.__pose.x, self.__pose.y)
        )
        for _ in range(len(rectangle_layer.corners) + 1):
            actions = self.move_to(current_corner.position)
            progress.extend(actions)
            current_corner = current_corner.next_corner
        return progress

    def move_to(self, position: Vector) -> List[HLAction]:
        x_difference = int(position.x - self.__pose.x)
        y_difference = int(position.y - self.__pose.y)

        actions = []

        if x_difference != 0:
            x_movement = Vector(x_difference, 0)
            actions.extend(
                self.move_along_1dimensional_vector(x_movement)
            )
        if y_difference != 0:
            y_movement = Vector(0, y_difference)
            actions.extend(
                self.move_along_1dimensional_vector(y_movement)
            )

        return actions

    def move_along_1dimensional_vector(self, vector: Vector):
        actions = []
        actions.extend(self.align_orientation(vector))
        for _ in range(abs(vector.sum())):
            move_forward = HLAction.MOVE_FORWARD
            self.__pose.apply_action(move_forward)
            actions.append(move_forward)
        return actions

    def align_orientation(self, vector: Vector):
        angle = self.__pose.get_directional_angle_to(vector)

        if angle >= 0:
            rotation_direction = 1
        else:
            rotation_direction = -1

        actions = []
        for _ in range(0, int(abs(angle)), 90):
            a = HLAction((0, 0, rotation_direction * 90))
            self.__pose.apply_action(a)
            actions.append(a)

        return actions
