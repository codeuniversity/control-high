from hlc.planner.helper import Vector, Pose, HLAction
from hlc.planner.maps import Layered2DMap, Layer
from typing import Tuple, List
from math import sqrt, acos, degrees
import numpy as np
import decimal


def generate_plan(target_map: Layered2DMap, start_pose=Pose(0, 0, 0)) -> List[HLAction]:

    max_layer_index = min(target_map.width, target_map.height) / 2

    robot_pose = start_pose.copy()
    plan = []
    while target_map.layer_index < max_layer_index:

        layer = target_map.generate_rectangle_layer()

        actions = progress_through_layer(layer, robot_pose)
        plan.extend(actions)

        target_map.switchLayer(target_map.layer_index + 1)

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
