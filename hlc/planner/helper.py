from enum import Enum


class Pose():

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self._orientation_vector = self._get_orientation_vector()

    def _get_orientation_vector(self):
        if self.theta == 0:
            return (0, 1)
        elif self.theta == 90:
            return (1, 0)
        elif abs(self.theta) == 180:
            return (0, -1)
        elif self.theta == -90:
            return (-1, 0)
        else:
            ValueError(
                "Theta is outside of the defined range: (90,-90,180,-180,0): {}".format(self.theta))

    def _update_orientation(self, new_theta):
        self.theta += new_theta
        if abs(self.theta) == 360:
            self.theta = 0
        elif self.theta == -270:
            self.theta = 90
        elif self.theta == 270:
            self.theta = -90
        self._orientation_vector = self._get_orientation_vector()

    def update(self, hl_action):
        self._update_orientation(hl_action.value[2])
        if hl_action.name == "MOVE_FORWARD":
            self.x += self._orientation_vector[0]
            self.y += self._orientation_vector[1]
        elif hl_action.name == "MOVE_BACKWARD":
            self.x -= self._orientation_vector[0]
            self.y -= self._orientation_vector[1]

    def __eq__(self, value):
        if isinstance(value, Pose):
            return self.to_tuple() == value.tuple()
        elif isinstance(value, tuple):
            return self.to_tuple() == value
        else:
            raise TypeError(
                "The operator == of Pose isn't defined \
                    for an object of type: {}".format(type(value)))

    def copy(self):
        return Pose(self.x, self.y, self.theta)

    def to_tuple(self):
        return (self.x, self.y, self.theta)

    def get_position(self):
        return (self.x, self.y)

    def add_tuple(self, other):
        return(self.x + other[0], self.y + other[1])


class HLAction(Enum):
    TURN_RIGHT = (0, 0, 90)
    TURN_LEFT = (0, 0, -90)

    MOVE_FORWARD = (0, 1, 0)
    MOVE_BACKWARD = (0, -1, 0)

    MOVE_SIDEWAYS_RIGHT = (1, 0, 0)
    MOVE_SIDEWAYS_LEFT = (-1, 0, 0)


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
