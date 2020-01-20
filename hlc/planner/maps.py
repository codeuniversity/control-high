from hlc.planner.helper import Vector
from typing import List, Tuple


class Map2D():
    def __init__(self, width: int, height: int, obstacle_positions: List[Tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacle_grid = self._generate_grid(obstacle_positions)

    def _generate_grid(self, obstacles_positions: List[Tuple[int, int]]):
        keys_grid = []

        for x in range(self.width):
            for y in range(self.height):
                keys_grid.append((x, y))

        grid = dict.fromkeys(keys_grid, None)
        for o in obstacles_positions:
            grid[o] = False
        return grid

    def get_obstacle(self, key):
        return self.obstacle_grid[key]

    def set_obstacle(self, key, value):
        self.obstacle_grid[key] = value

    def obstacle_grid_values(self):
        return self.obstacle_grid.values()


class Layered2DMap(Map2D):

    def __init__(self, width: int, height: int, obstacle_positions: List[Vector], layer_index=0):
        super().__init__(width, height, obstacle_positions)
        self.layer_index = layer_index

    def generate_rectangle_layer(self):
        min_width = self.layer_index
        min_height = self.layer_index
        max_width = self.width - self.layer_index - 1
        max_height = self.height - self.layer_index - 1

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
        self.corners = []

        for position in corner_positions:
            self.corners.append(Corner(position))

        self.corners[0].previous_corner = self.corners[-1]
        self.corners[-1].next_corner = self.corners[0]
        for i in range(len(self.corners) - 1):
            self.corners[i].next_corner = self.corners[i+1]
        for i in range(1, len(self.corners)):
            self.corners[i].previous_corner = self.corners[i-1]

    def get_closest_corner(self, position: Vector) -> Corner:
        min_distance = float("inf")
        closest_corner = None
        for c in self.corners:
            distance = position.get_distance_to(c.position)
            if distance < min_distance:
                closest_corner = c
                min_distance = distance
        return closest_corner
