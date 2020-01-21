from enum import Enum
import numpy as np
from math import cos, acos, sin, radians, degrees


class HLAction(Enum):
    TURN_RIGHT = (0, 0, 90)
    TURN_LEFT = (0, 0, -90)

    MOVE_FORWARD = (0, 1, 0)
    MOVE_BACKWARD = (0, -1, 0)


class Pose():

    def __init__(self, x: int, y: int, angle=0, orientation=None):
        self.position = Vector(x, y)
        self.default_orientation = Vector(0, 1)
        if orientation is not None:
            self.orientation = orientation
        else:
            self.orientation = self.default_orientation
            self.orientation = self.orientation.rotate(angle)

    def apply_action(self, action: HLAction):
        sideway_steps = action.value[0]
        straight_steps = action.value[1]
        rotation = action.value[2]

        self.orientation = self.orientation.rotate(rotation)

        x_axis = self.orientation.rotate(90)
        y_axis = self.orientation

        straight_movement = y_axis.multiply_with_scalar(straight_steps)
        sideway_movement = x_axis.multiply_with_scalar(sideway_steps)
        movement = straight_movement + sideway_movement

        self.position += movement

    def get_directional_angle_to(self, vector):
        y_axis = self.orientation
        x_axis = self.orientation.rotate(90)

        angle_y_axis = vector.get_angle_to(y_axis)
        angle_x_axis = vector.get_angle_to(x_axis)
        if angle_x_axis <= 90:
            rotation_direction = 1
        else:
            rotation_direction = -1
        return angle_y_axis * rotation_direction

    def copy(self):
        return Pose(self.position.get_x(), self.position.get_y(), orientation=self.orientation)

    def get_position(self):
        return tuple(self.position.coordinates)


class Vector():
    def __init__(self, x, y):
        self.coordinates = np.array((x, y))

    def get_norm(self):
        return np.linalg.norm(self.coordinates)

    def get_angle_to(self, other):
        norm_of_self = self.get_norm()
        norm_of_other = other.get_norm()
        dot_product = np.dot(self.coordinates, other.coordinates)
        cos_angle = dot_product / norm_of_self * norm_of_other
        angle = degrees(acos(cos_angle))
        return round(angle, 5)

    def normalize(self):
        norm_of_self = np.linalg.norm(self.coordinates)
        return self.coordinates / norm_of_self

    def get_distance_to(self, other):
        vector_to_other = self.coordinates - other.coordinates
        distance = np.sqrt(np.power(vector_to_other, 2).sum())
        return distance

    def _get_rotation_matrix(self, angle: int):
        rotate_clockwise = angle >= 0
        rad_angle = radians(abs(angle))
        rotation_matrix = np.array([
            [round(cos(rad_angle), 5), -round(sin(rad_angle), 5)],
            [round(sin(rad_angle), 5), round(cos(rad_angle))]
        ])
        if rotate_clockwise:
            rotation_matrix = np.linalg.inv(rotation_matrix)
        return rotation_matrix

    def rotate(self,  angle: int):
        if angle == 0:
            return Vector(self.get_x(), self.get_y())
        rotation_matrix = self._get_rotation_matrix(angle)
        new_coordinates = np.dot(rotation_matrix, self.coordinates)
        return Vector(new_coordinates[0], new_coordinates[1])

    def sum(self):
        return np.sum(self.coordinates)

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def __iadd__(self, other):
        self.coordinates = self.coordinates + other.coordinates
        return self

    def __add__(self, other):
        new_coordinates = self.coordinates + other.coordinates
        return Vector(new_coordinates[0], new_coordinates[1])

    def multiply_with_scalar(self, scalar):
        new_x, new_y = self.coordinates * scalar
        return Vector(new_x, new_y)
