import math
from hlc.config.constants import *
from hlc.helpers.planner import Position


def plan(grid_dimension, start_pos = (0, 0), layer = 0, orientation = FORWARD):
    start_pos = Position(start_pos)
    pos = start_pos.copy()
    start_pos.update((1, 0))
    plan = []

    max_layer = max(grid_dimension) // 2

    while layer < max_layer:

        plan.append(MOVE_FORWARD)
        pos.update(orientation)


        if pos == start_pos:
            plan.append(TURN_RIGHT)
            plan.append(MOVE_FORWARD)
            pos.update(FORWARD)
            layer += 1
            start_pos = pos.copy().update((1, 0))
            orientation = FORWARD
        elif pos.x == layer and pos.y == grid_dimension[1]-layer:
            plan.append(TURN_RIGHT)
            orientation = RIGHT
        elif pos.x == grid_dimension[0]-layer and pos.y == grid_dimension[1]-layer:
            plan.append(TURN_RIGHT)
            orientation = BACKWARD
        elif pos.x == grid_dimension[0]-layer and pos.y == layer:
            plan.append(TURN_RIGHT)
            orientation = LEFT

    if grid_dimension[0] != grid_dimension[1] and layer == max_layer:
        if grid_dimension[0] % 2 == 1:
            plan.append(TURN_RIGHT)
            while pos.x < grid_dimension[0]-layer:
                plan.append(MOVE_FORWARD)
                pos.update(RIGHT)
        else:
            while pos.y < grid_dimension[1]-layer:
                plan.append(MOVE_FORWARD)
                pos.update(FORWARD)

    return plan
