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
