from enum import Enum


class RenameRule(Enum):
    """
    The rule about which window is used to rename the workspace when workspace
    rename is triggered.

    FIRST_WINDOW: Workspace is named after the window which happens to be first in the workspace's tree hierarchy.
    TODO: FOCUSED_WINDOW might make sense as an alternative at least when the workspace is focused?
    """
    FIRST_WINDOW = 1


rename_rule = RenameRule.FIRST_WINDOW

# Workspaces which have dynamically changing icons.
dynamic_workspace_names = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
