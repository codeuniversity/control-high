from hlc.planner.helper import Vector
from typing import List, Tuple


class Map2D():
    def __init__(self, width: int, height: int, obstacle_positions: List[Tuple[int, int]]):
        self._width = width
        self._height = height
        self._obstacle_grid = self._generate_grid(obstacle_positions)

    def _generate_grid(self, obstacles_positions: List[Tuple[int, int]]):
        keys_grid = []

        for x in range(self._width):
            for y in range(self._height):
                keys_grid.append((x, y))

        grid = dict.fromkeys(keys_grid, None)
        for o in obstacles_positions:
            grid[o] = False
        return grid

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get_obstacle(self, key):
        return self._obstacle_grid[key]

    def set_obstacle(self, key, value):
        self._obstacle_grid[key] = value

    def get_all_positions(self):
        return self._obstacle_grid.keys()


class Layered2DMap(Map2D):

    def __init__(self, width: int, height: int, obstacle_positions: List[Vector], layer_index=0):
        super().__init__(width, height, obstacle_positions)
        self.layer_index = layer_index

    def generate_rectangle_layer(self):
        min_width = self.layer_index
        min_height = self.layer_index
        max_width = self._width - self.layer_index - 1
        max_height = self._height - self.layer_index - 1

        corner_positions = [
            Vector(min_width, min_height),
            Vector(min_width, max_height),
            Vector(max_width, max_height),
            Vector(max_width, min_height)
        ]
        return Layer(corner_positions)


class Corner():
    def __init__(self, position: Vector):
        self.position = position
        self.next_corner: Corner
        self.previous_corner: Corner


class Layer():
    def __init__(self, corner_positions: List[Vector]):
        self.__corners = []

        for position in corner_positions:
            self.__corners.append(Corner(position))

        self.__corners[0].previous_corner = self.__corners[-1]
        self.__corners[-1].next_corner = self.__corners[0]
        for i in range(len(self.__corners) - 1):
            self.__corners[i].next_corner = self.__corners[i+1]
        for i in range(1, len(self.__corners)):
            self.__corners[i].previous_corner = self.__corners[i-1]

    @property
    def corners(self):
        return self.__corners.copy()

    def get_closest_corner(self, position: Vector) -> Corner:
        min_distance = float("inf")
        closest_corner = None
        for c in self.__corners:
            distance = position.get_distance_to(c.position)
            if distance < min_distance:
                closest_corner = c
                min_distance = distance
        return closest_corner
