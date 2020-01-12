# from hlc.config.constants import *
from hlc.planner.helper import Position, Pose, HLAction
from typing import Tuple, List

Corner = Tuple[int, int]


class Map2D():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Layered2DMap(Map2D):

    def __init__(self, width: int, height: int, layer_index: int):
        self.width = width
        self.height = height
        self.layer_index = layer_index
        self._update_all_layer_corners()

    def _get_left_bottom_layer_corner(self) -> Corner:
        return (self.layer_index, self.layer_index)

    def _get_left_upper_layer_corner(self) -> Corner:
        return (self.layer_index, self.height - self.layer_index - 1)

    def _get_right_upper_layer_corner(self) -> Corner:
        return (self.width - self.layer_index - 1, self.height - self.layer_index - 1)

    def _get_right_bottom_layer_corner(self) -> Corner:
        return (self.width - self.layer_index - 1, self.layer_index)

    def _update_all_layer_corners(self):
        self.left_bottom_layer_corner = self._get_left_bottom_layer_corner()
        self.left_upper_layer_corner = self._get_left_upper_layer_corner()
        self.right_upper_layer_corner = self._get_right_upper_layer_corner()
        self.right_bottom_layer_corner = self._get_right_bottom_layer_corner()

    def switchLayer(self, layer_index: int):
        self.layer_index = layer_index
        self._update_all_layer_corners()


def apply_actions(actions: List[HLAction], robot_pose: Pose, plan: List[HLAction]):
    for a in actions:
        plan.append(a)
        robot_pose.update(a)


def update_position(pose: Pose, new_actions: List[HLAction]):
    for action in new_actions:
        pose.update(action)


def plan(grid_width: int, grid_height: int, start_pose=Pose(0, 0, 0), layer_index=0) -> List[HLAction]:
    robot_pose = start_pose.copy()
    plan = []
    final_layer_position = start_pose.add_tuple((1, 0))

    layer_map = Layered2DMap(grid_width, grid_height, layer_index)

    max_layer_index = min(grid_height, grid_width) // 2

    while layer_map.layer_index < max_layer_index:

        actions = progress_through_layer(
            layer_map, robot_pose, final_layer_position)
        plan.extend(actions)

        switch_layer_actions = [HLAction.TURN_RIGHT, HLAction.MOVE_FORWARD]
        apply_actions(switch_layer_actions, robot_pose, plan)
        final_layer_position = get_new_final_layer_position(robot_pose)
        layer_map.switchLayer(layer_map.layer_index + 1)

    if grid_width != grid_height and layer_map.layer_index == max_layer_index:
        if grid_width % 2 == 1:
            apply_actions([HLAction.TURN_RIGHT], robot_pose, plan)
            while robot_pose.x < grid_width - layer_map.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)
        else:
            while robot_pose.y < grid_height - layer_map.layer_index:
                apply_actions([HLAction.MOVE_FORWARD], robot_pose, plan)

    return plan


def get_new_final_layer_position(robot_pose: Pose) -> Tuple[int, int]:
    return robot_pose.copy().add_tuple((1, 0))


def progress_through_layer(layer_map: Layered2DMap, robot_pose: Pose, final_layer_position: Tuple[int, int]) -> List[HLAction]:
    progress = []
    while robot_pose.get_position() != final_layer_position:
        apply_actions([HLAction.MOVE_FORWARD], robot_pose, progress)

        if layer_map.left_upper_layer_corner == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)
        elif layer_map.right_upper_layer_corner == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)
        elif layer_map.right_bottom_layer_corner == robot_pose.get_position():
            apply_actions([HLAction.TURN_RIGHT], robot_pose, progress)

    return progress
