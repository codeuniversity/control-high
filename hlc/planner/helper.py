from enum import Enum
import numpy as np
from math import cos, acos, sin, radians


class HLAction(Enum):
    TURN_RIGHT = (0, 0, 90)
    TURN_LEFT = (0, 0, -90)

    MOVE_FORWARD = (0, 1, 0)
    MOVE_BACKWARD = (0, -1, 0)


class Pose():

    def __init__(self, x: int, y: int, angle=0, orientation=None):
        self.position = np.array([x, y], dtype=np.float64)
        self.default_orientation = np.array([0, 1], dtype=np.float64)
        if orientation is not None:
            self.orientation = orientation
        else:
            self.orientation = self.default_orientation
            self.orientation = self.rotate_vector(self.orientation, angle)

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

    def _get_angle_between_vectors(self, vector1: np.ndarray, vector2: np.ndarray):
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)
        cos_angle = np.dot(vector1, vector2) / norm_vector1 * norm_vector2
        return round(acos(cos_angle), 5)

    def rotate_vector(self, vector: np.ndarray, angle: int):
        if angle == 0:
            return vector
        rotation_matrix = self._get_rotation_matrix(angle)
        return np.dot(rotation_matrix, vector)

    def apply_action(self, action: HLAction):
        sideway_movement = action.value[0]
        straight_movement = action.value[1]
        rotation = action.value[2]

        new_orientation = self.rotate_vector(self.orientation, rotation)
        self.orientation = new_orientation

        x_axis = self.rotate_vector(self.orientation, 90)
        y_axis = self.orientation
        movement = y_axis * straight_movement + x_axis * sideway_movement
        self.position += movement

    def __eq__(self, value):
        position_equal = np.all(self.position == value.position)
        orientation_equal = np.all(self.orientation == value.orientation)
        return position_equal and orientation_equal

    def copy(self):
        return Pose(self.position[0], self.position[1], orientation=self.orientation)

    def get_position(self):
        return tuple(self.position)

    def add_position(self, other):
        return (
            self.position[0] + other[0],
            self.position[1] + other[1],
        )
