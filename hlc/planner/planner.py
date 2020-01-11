# from hlc.config.constants import *
from hlc.planner.helper import Position, Pose, HLAction


def get_layer_corners(map_dimensions, layer_index):
    left_bottom_corner = (layer_index, layer_index)
    left_upper_corner = (layer_index, map_dimensions[1] - layer_index)
    right_upper_corner = (
        map_dimensions[0] - layer_index,
        map_dimensions[1] - layer_index)
    right_bottom_corner = (map_dimensions[0]-layer_index, layer_index)

    return left_bottom_corner, left_upper_corner, right_upper_corner, right_bottom_corner


def apply_actions(actions, position, plan):
    for a in actions:
        plan.append(a)
        position.update(a)


def update_position(pose, new_actions):
    for action in new_actions:
        pose.update(action)


def plan(grid_dimension, start_pose=Pose(0, 0, 0), layer_index=0,):
    robot_pose = start_pose.copy()
    plan = []
    final_layer_position = start_pose.add_tuple((1, 0))

    corners = get_layer_corners(grid_dimension, layer_index)
    _, left_upper_corner, right_upper_corner, right_bottom_corner = corners

    max_layer_index = max(grid_dimension) // 2

    while layer_index < max_layer_index:

        apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

        if robot_pose.get_position() == final_layer_position:
            switch_layer_actions = [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD]
            plan.extend(switch_layer_actions)
            update_position(robot_pose, switch_layer_actions)
            final_layer_position = get_new_final_layer_position(robot_pose)

            layer_index += 1
            corners = get_layer_corners(grid_dimension, layer_index)
            _, left_upper_corner, right_upper_corner, right_bottom_corner = corners
        elif (robot_pose.x, robot_pose.y) == left_upper_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif (robot_pose.x, robot_pose.y) == right_upper_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif (robot_pose.x, robot_pose.y) == right_bottom_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)

    if grid_dimension[0] != grid_dimension[1] and layer_index == max_layer_index:
        if grid_dimension[0] % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
            while robot_pose.x < grid_dimension[0] - layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)
        else:
            while robot_pose.y < grid_dimension[1] - layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

    return plan


def get_new_final_layer_position(robot_pose):
    return robot_pose.copy().add_tuple((1, 0))
