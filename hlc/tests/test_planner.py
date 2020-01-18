from hlc.tests.helper import create_solution_grid, check_solution_grid
from hlc.planner.helper import Pose


def test_evenly_square_empty_map():
    grid = create_solution_grid(6, 6, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_horizontal_rectangle_empty_map():
    grid = create_solution_grid(8, 6, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_vertical_rectangle_empty_map():
    grid = create_solution_grid(4, 8, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_with_point_layer():
    grid = create_solution_grid(7, 7, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_with_line_layer():
    grid = create_solution_grid(9, 7, Pose(0, 0, 0))
    check_solution_grid(grid, [])


def test_empty_map_6x6_different_starting_point():
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
