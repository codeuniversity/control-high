from enum import Enum
from hlc.plan.planner import plan
from hlc.plan.grid_generator import generate_grid


class RePlanner():
    def __init__(self, point_cloud, current_position):
        self.point_cloud = point_cloud
        self.current_position = current_position


    def run(self):
        grid = generate_grid(self.point_cloud)

        return plan(grid, self.current_position)
