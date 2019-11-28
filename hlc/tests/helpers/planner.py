from hlc.config.constants import *

def right_turn(orientation):
    if orientation == FORWARD:
        orientation = RIGHT
    elif orientation == RIGHT:
        orientation = BACKWARD
    elif orientation == BACKWARD:
        orientation  = LEFT
    elif orientation == LEFT:
        orientation = FORWARD

    return orientation


def generate_grid(grid_dimension):
    keys_grid = []

    for x in range(grid_dimension[0] + 1):
        for y in range(grid_dimension[1] + 1):
            keys_grid.append((x, y))

    return dict.fromkeys(keys_grid, None)


def navigate_grid(plan, grid, position):
    orientation = FORWARD

    for action in plan:
        if action == TURN_RIGHT:
            orientation = right_turn(orientation)
            grid[position.current()] = True
        elif action == MOVE_FORWARD:
            position.update(orientation)
            grid[position.current()] = True

    return grid
