class Position():
    def __init__(self, coordinates=(0, 0)):
        self.x, self.y = coordinates

    def __eq__(self, value):
        if isinstance(value, Position):
            return self.current() == value.current()
        elif isinstance(value, tuple):
            return self.current() == value
        else:
            raise TypeError('Parameter has to be of class Position or of type tuple.')

    def current(self):
        return (self.x, self.y)

    def copy(self):
        return Position(self.current())

    def update(self, action, operationIsAdd=True):
        new_x, new_y = action

        if operationIsAdd:
            self.x += new_x
            self.y += new_y
        else:
            self.x -= new_x
            self.y -= new_y

        return (self.x, self.y)


def layer_pos(grid_dimension, layer):
    left_layer = []
    right_layer = []
    top_layer = []
    bottom_layer = []

    for i in range(grid_dimension[1]):
        left_layer.append((layer, i))

    for j in range(grid_dimension[1]):
        right_layer.append(grid_dimension[1] - layer, j)

    for k in range(grid_dimension[0]):
        top_layer.append(k, grid_dimension[0] - layer)

    for l in range(grid_dimension[0]):
        bottom_layer.append(l, layer)

    return left_layer, right_layer, top_layer, bottom_layer
