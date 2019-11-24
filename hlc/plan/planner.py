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


class Position():
    def __init__(self, coordiantes):
        self.x, self.y = coordiantes

    def current(self):
        return (self.x, self.y)

    def update(self, action, operationIsAdd=True):
        new_x, new_y = action
        if operationIsAdd:
            self.x += action[0]
            self.y += action[1]
        else:
            self.x -= action[0]
            self.y -= action[1]

        return (self.x, self.y)


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


def plan(grid, grid_dimension, start_pos = (0,0), layer = 0, orientation = FORWARD):
    pos = Position(start_pos)
    plan =  []

    max_layer = max(grid_dimension) // 2

    while layer < max_layer:

        plan.append(MOVE_FORWARD)
        pos.update(orientation)

        if pos.current() == Position(start_pos).update((1, 0)):
            plan.append(TURN_RIGHT)
            plan.append(MOVE_FORWARD)
            pos.update(FORWARD)
            layer += 1
            start_pos = pos.current()
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
