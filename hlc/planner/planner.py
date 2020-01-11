# from hlc.config.constants import *
from hlc.planner.helper import Position, Pose, HLAction


def apply_actions(actions, position, plan):
    for a in actions:
        plan.append(a)
        position.update(a)


def update_position(pose, new_actions):
    for action in new_actions:
        pose.update(action)


def plan(grid_dimension, start_pose=Pose(0, 0, 0), layer=0,):
    robot_pose = start_pose.copy()
    plan = []
    final_layer_position = start_pose.add_tuple((1, 0))

    max_layer = max(grid_dimension) // 2

    while layer < max_layer:

        apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

        if robot_pose.get_position() == final_layer_position:
            switch_layer_actions = [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD]
            plan.extend(switch_layer_actions)
            update_position(robot_pose, switch_layer_actions)
            final_layer_position = get_new_final_layer_position(robot_pose)
            layer += 1
        elif robot_pose.x == layer and robot_pose.y == grid_dimension[1] - layer:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif robot_pose.x == grid_dimension[0] - layer and robot_pose.y == grid_dimension[1] - layer:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif robot_pose.x == grid_dimension[0] - layer and robot_pose.y == layer:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)

    if grid_dimension[0] != grid_dimension[1] and layer == max_layer:
        if grid_dimension[0] % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
            while robot_pose.x < grid_dimension[0] - layer:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)
        else:
            while robot_pose.y < grid_dimension[1] - layer:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

    return plan


def get_new_final_layer_position(robot_pose):
    return robot_pose.copy().add_tuple((1, 0))
