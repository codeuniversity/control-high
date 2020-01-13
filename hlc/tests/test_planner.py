from hlc.planner import planner
from hlc.planner.planner import plan
from hlc.planner.helper import Pose, HLAction
from hlc.tests.helper import create_solution_grid, check_solution_grid
from typing import List, Tuple


def test_empty_map_6x6():
    grid = create_solution_grid(6, 6, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_8x6():
    grid = create_solution_grid(8, 6, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_7x7():
    grid = create_solution_grid(7, 7, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_9x7():
    grid = create_solution_grid(9, 7, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_8x4():
    grid = create_solution_grid(8, 4, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_8x5():
    grid = create_solution_grid(8, 5, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_6x6_starting_right_top():
    grid = create_solution_grid(6, 6, Pose(6, 6, -90))
    check_solution_grid(grid, [])


def test_empty_map_6x6_wrong_orientation():
    grid = create_solution_grid(6, 6, Pose(0, 0, -90))
    check_solution_grid(grid, [])


def test_one_obstacle_6x6():
    obstacles = [(1, 2)]
    grid = create_solution_grid(6, 6, Pose(0, 0, 0), obstacles)
    check_solution_grid(grid, obstacles)


def test_multiple_obstacle_6x6():
    obstacles = [(2, 1), (3, 4), (5, 1), (5, 4)]
    grid = create_solution_grid(6, 6, Pose(0, 0, 0), obstacles)
    check_solution_grid(grid, obstacles)


def test_dead_end_6x6():
    obstacles = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    grid = create_solution_grid(6, 6, Pose(0, 0, 0), obstacles)
    check_solution_grid(grid, obstacles)
