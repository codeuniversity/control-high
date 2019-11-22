import math

FORWARD = (0, 1)
RIGHT_FORWARD = (1, 1)
RIGHT = (1, 0)
RIGHT_BACKWARD = (1, -1)
BACKWARD = (0, -1)
LEFT_BACKWARD = (-1, -1)
LEFT = (-1, 0)
LEFT_FORWARD = (-1, 1)

MOVE_FORWARD = 'move forward'
TURN_RIGHT = 'turn right 90 degrees'


def add_pos_tuple(t1, t2):
    new_x = t1[0] + t2[0]
    new_y = t1[1] + t2[1]
    return (new_x, new_y)


def sub_pos_tuple(t1, t2):
    new_x = t1[0] - t2[0]
    new_y = t1[1] - t2[1]
    return (new_x, new_y)


def layer_pos(grid_dimension, layer):
    left_layer = []
    right_layer = []
    top_layer = []
    bottom_layer = []

    for i in range(grid_dimension[1]):
        left_layer.append((layer, i))

    for j in range(grid_dimension[1]):
        right_layer.append(grid_dimension[1] - layer, j)

    for k in range(grid_dimension[0]):
        top_layer.append(k, grid_dimension[0] - layer)

    for l in range(grid_dimension[0]):
        bottom_layer.append(l, layer)

    return left_layer, right_layer, top_layer, bottom_layer


def update_pos(pos, action):
    new_pos = add_pos_tuple(pos, action)
    return new_pos


def plan(grid, grid_dimension:(int, int), start_pos = (0,0), layer = 0, orientation = FORWARD):
    pos = start_pos
    plan =  []

    max_layer = math.floor(max(grid_dimension)/2)
    max_layer = int(max_layer)

    while layer < max_layer:

        plan.append(MOVE_FORWARD)
        pos = update_pos(pos, orientation)

        if pos == add_pos_tuple(start_pos, (1,0)):
            plan.append(TURN_RIGHT)
            plan.append(MOVE_FORWARD)
            pos = add_pos_tuple(pos, FORWARD)
            layer += 1
            start_pos = pos
            orientation = FORWARD
        elif pos[1] == layer and pos[0] == grid_dimension[0]-layer:
            plan.append(TURN_RIGHT)
            orientation = LEFT
        elif pos[0] == grid_dimension[0]-layer and pos[1] == grid_dimension[1]-layer:
            plan.append(TURN_RIGHT)
            orientation = BACKWARD
        elif pos[1] == grid_dimension[1]-layer and pos[0] == layer:
            plan.append(TURN_RIGHT)
            orientation = RIGHT

    if grid_dimension[0] != grid_dimension[1] and layer == max_layer:
        if grid_dimension[0] % 2 == 1:
            plan.append(TURN_RIGHT)
            while pos[0] < grid_dimension[0]-layer:
                plan.append(MOVE_FORWARD)
                pos = add_pos_tuple(pos, RIGHT)
        else:
            while pos[1] < grid_dimension[1]-layer:
                plan.append(MOVE_FORWARD)
                pos = add_pos_tuple(pos, FORWARD)

    return plan
