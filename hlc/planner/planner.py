# from hlc.config.constants import *
from hlc.planner.helper import Position, Pose, HLAction


def apply_actions(actions, position, plan):
    for a in actions:
        plan.append(a)
        position.update(a)


def plan(grid_dimension, start_pose=Pose(0, 0, 0), layer=0,):
    pos = start_pose.copy()
    plan = []

    max_layer = max(grid_dimension) // 2

    while layer < max_layer:

        apply_actions([HLAction.MOVE_FORWARD], pos, plan)

        if pos.get_position() == start_pose.add_tuple((1, 0)):
            apply_actions(
                [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD], pos, plan)
            # start_pos = pos.copy().update((1, 0))
            start_pose = pos.copy()
            layer += 1
        elif pos.x == layer and pos.y == grid_dimension[1] - layer:
            apply_actions([HLAction.TURN_RIGHT], pos, plan)
        elif pos.x == grid_dimension[0] - layer and pos.y == grid_dimension[1] - layer:
            apply_actions([HLAction.TURN_RIGHT], pos, plan)
        elif pos.x == grid_dimension[0] - layer and pos.y == layer:
            apply_actions([HLAction.TURN_RIGHT], pos, plan)

    if grid_dimension[0] != grid_dimension[1] and layer == max_layer:
        if grid_dimension[0] % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], pos, plan)
            while pos.x < grid_dimension[0] - layer:
                apply_actions([HLAction.MOVE_FORWARD], pos, plan)
        else:
            while pos.y < grid_dimension[1] - layer:
                apply_actions([HLAction.MOVE_FORWARD], pos, plan)

    return plan
