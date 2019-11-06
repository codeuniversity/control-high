class Action(Enum):
    FORWARD = (0, 1)
    RIGHT_FORWARD = (1, 1)
    RIGHT = (1, 0)
    RIGHT_BACKWARD = (1, -1)
    BACKWARD = (0, -1)
    LEFT_BACKWARD = (-1, -1)
    LEFT = (-1, 0)
    LEFT_FORWARD = (-1, 1)

def add_pos_tuple(t1, t2):
    new_x = t1[0] + t2[0]
    new_y = t1[1] + t2[1]
    return (new_x, new_y)


def move_one_unit_forward():
    pass


def turn_left():
    pass


def turn_right():
    pass


def plan(grid, current_position):
    number_of_possible_points = grid.values().count(None)

    # Points on map:
    #     None means unexplored
    #     False means blocked
    #     True means explored
    #
    # Uncertainties with this method:
    #     This concept will require the knowledge of the current orientation.
    #
    # This concept will not use absolute step-directions, but rather relative ones.
    # This is why the orientation is needed. For this 'planning'-algorithm though,
    #   I think this method makes more sense.
    # This concept does not utilize layers, because in the tired state I am in
    #   I can not think of a way to easily implement these layers and for the cases I
    #   I came up with that can actually occur this hacky concept works.
    #
    # @Selma feel free to look at this and then start a new. I am open for other concepts.
    #
    # And yes I know this is horrible. Especially since it is hacky AND NOT EVEN WORKING
    #   since half of this is not yet written functions with the hope that this logic works.

    left_point = "Either None, True or False"
    next_point = "Either None, True or False"
    right_point = "Either None, True or False"


    while number_of_possible_points > 0:
        # This point is for the scenarion where the 'else' does not work. See trello card for picture (p2).
        if left_point is None and right_point is None and next_point is not None:
            turn_left()
            move_one_unit_forward()
            number_of_possible_points -= 1
            while next_point is None:
                move_one_unit_forward()
                number_of_possible_points -= 1
            turn_right()
            turn_right()
            while next_point is not False:
                if next_point is True:
                    move_one_unit_forward()
                else:
                    move_one_unit_forward()
                    number_of_possible_points -= 1
        elif left_point is None:
            turn_left()
            move_one_unit_forward()
            number_of_possible_points -= 1
        elif next_point is not None and right_point is None:
            turn_right()
            move_one_unit_forward()
            number_of_possible_points -= 1
        elif next_point is None:
            move_one_unit_forward()
            number_of_possible_points -= 1
        # This is for when the simple movement options do not work anymore. See trello card for picture (p1).
        else:
            trapped = True
            while trapped:
                if left_point is None:
                    turn_left()
                    trapped = False
                elif next_point is False:
                    turn_right()
                    move_one_unit_forward()
                elif next_point is True:
                    move_one_unit_forward()
                else:
                    pass


    # The update of the plan array will either have to be added in the loop or in the move_one_unit_forward function.
    plan = [(0, 1), (1, 1)]

    return plan
