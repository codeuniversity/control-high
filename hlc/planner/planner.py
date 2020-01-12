# from hlc.config.constants import *
from hlc.planner.helper import Position, Pose, HLAction


class Map2D():
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Layered2DMap(Map2D):

    def __init__(self, width, height, layer_index):
        self.width = width
        self.height = height
        self.layer_index = layer_index
        self._update_all_layer_corners()

    def _get_left_bottom_layer_corner(self):
        return (self.layer_index, self.layer_index)

    def _get_left_upper_layer_corner(self):
        return (self.layer_index, self.height - self.layer_index - 1)

    def _get_right_upper_layer_corner(self):
        return (self.width - self.layer_index - 1, self.height - self.layer_index - 1)

    def _get_right_bottom_layer_corner(self):
        return (self.width - self.layer_index - 1, self.layer_index)

    def _update_all_layer_corners(self):
        self.left_bottom_layer_corner = self._get_left_bottom_layer_corner()
        self.left_upper_layer_corner = self._get_left_upper_layer_corner()
        self.right_upper_layer_corner = self._get_right_upper_layer_corner()
        self.right_bottom_layer_corner = self._get_right_bottom_layer_corner()

    def switchLayer(self, layer_index):
        self.layer_index = layer_index
        self._update_all_layer_corners()


def apply_actions(actions, position, plan):
    for a in actions:
        plan.append(a)
        position.update(a)


def update_position(pose, new_actions):
    for action in new_actions:
        pose.update(action)


def plan(grid_width, grid_height, start_pose=Pose(0, 0, 0), layer_index=0,):
    robot_pose = start_pose.copy()
    plan = []
    final_layer_position = start_pose.add_tuple((1, 0))

    layerMap = Layered2DMap(grid_width, grid_height, layer_index)

    max_layer_index = min(grid_height, grid_width) // 2

    while layerMap.layer_index < max_layer_index:

        apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

        if robot_pose.get_position() == final_layer_position:
            switch_layer_actions = [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD]
            plan.extend(switch_layer_actions)
            update_position(robot_pose, switch_layer_actions)
            final_layer_position = get_new_final_layer_position(robot_pose)
            layerMap.switchLayer(layerMap.layer_index + 1)
        elif robot_pose.get_position() == layerMap.left_upper_layer_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif robot_pose.get_position() == layerMap.right_upper_layer_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
        elif robot_pose.get_position() == layerMap.right_bottom_layer_corner:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)

    if grid_width != grid_height and layerMap.layer_index == max_layer_index:
        if grid_width % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
            while robot_pose.x < grid_width - layerMap.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)
        else:
            while robot_pose.y < grid_height - layerMap.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

    return plan


def get_new_final_layer_position(robot_pose):
    return robot_pose.copy().add_tuple((1, 0))
