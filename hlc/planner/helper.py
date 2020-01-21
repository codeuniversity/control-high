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
        self.__position = Vector(x, y)
        default_orientation = Vector(0, 1)
        if orientation is not None:
            self.__orientation = orientation
        else:
            self.__orientation = default_orientation
            self.__orientation = self.__orientation.rotate(angle)

    def apply_action(self, action: HLAction):
        sideway_steps = action.value[0]
        straight_steps = action.value[1]
        rotation = action.value[2]

        self.__orientation = self.__orientation.rotate(rotation)

        x_axis = self.__orientation.rotate(90)
        y_axis = self.__orientation

        straight_movement = y_axis.multiply_with_scalar(straight_steps)
        sideway_movement = x_axis.multiply_with_scalar(sideway_steps)
        movement = straight_movement + sideway_movement

        self.__position += movement

    def get_directional_angle_to(self, vector: 'Vector') -> int:
        y_axis = self.__orientation
        x_axis = self.__orientation.rotate(90)

        angle_y_axis = vector.get_angle_to(y_axis)
        angle_x_axis = vector.get_angle_to(x_axis)
        if angle_x_axis <= 90:
            rotation_direction = 1
        else:
            rotation_direction = -1
        return angle_y_axis * rotation_direction

    def copy(self) -> 'Pose':
        return Pose(self.x, self.y, orientation=self.__orientation)

    @property
    def y(self):
        return self.__position.y

    @property
    def x(self):
        return self.__position.x


class Vector():
    def __init__(self, x, y):
        # Types for x,y are not specified to allow dynamic typing
        # and therefore the Vector-class to encapsulated mutliple
        # types of data
        self.__coordinates = np.array((x, y))

    def rotate(self,  angle: int) -> 'Vector':
        if angle == 0:
            return Vector(self.x, self.y)
        rotation_matrix = self._get_rotation_matrix(angle)
        new_coordinates = np.dot(rotation_matrix, self.__coordinates)
        return Vector(new_coordinates[0], new_coordinates[1])

    def _get_rotation_matrix(self, angle: int) -> np.ndarray:
        rotate_clockwise = angle >= 0
        rad_angle = radians(abs(angle))
        rotation_matrix = np.array([
            [round(cos(rad_angle), 5), -round(sin(rad_angle), 5)],
            [round(sin(rad_angle), 5), round(cos(rad_angle))]
        ])
        if rotate_clockwise:
            rotation_matrix = np.linalg.inv(rotation_matrix)
        return rotation_matrix

    def get_angle_to(self, other: 'Vector') -> float:
        norm_of_self = self.get_norm()
        norm_of_other = other.get_norm()
        dot_product = np.dot(self.__coordinates, other.get_np_coordinates())
        cos_angle = dot_product / norm_of_self * norm_of_other
        angle = degrees(acos(cos_angle))
        return round(angle, 5)

    def get_distance_to(self, other: 'Vector') -> float:
        vector_to_other = self.__coordinates - other.get_np_coordinates()
        distance = np.sqrt(np.power(vector_to_other, 2).sum())
        return distance

    def normalize(self) -> 'Vector':
        return self.__coordinates / self.get_norm()

    def get_norm(self) -> float:
        return np.linalg.norm(self.__coordinates)

    def multiply_with_scalar(self, scalar):
        new_x, new_y = self.__coordinates * scalar
        return Vector(new_x, new_y)

    def sum(self) -> float:
        return np.sum(self.__coordinates)

    def get_np_coordinates(self):
        return np.copy(self.__coordinates)

    @property
    def x(self):
        return self.__coordinates[0]

    @x.setter
    def x(self, value: int):
        self.__coordinates[0] = value

    @property
    def y(self):
        return self.__coordinates[1]

    @y.setter
    def y(self, value: int):
        self.__coordinates[1] = value

    def __iadd__(self, other: 'Vector') -> 'Vector':
        self.__coordinates = self.__coordinates + other.get_np_coordinates()
        return self

    def __add__(self, other: 'Vector') -> 'Vector':
        new_coordinates = self.__coordinates + other.get_np_coordinates()
        return Vector(new_coordinates[0], new_coordinates[1])
