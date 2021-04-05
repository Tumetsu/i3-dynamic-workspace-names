from enum import Enum


class RenameRule(Enum):
    """
    The rule about which window is used to rename the workspace when workspace
    rename is triggered.

    LATEST_WINDOW: Workspace is named after the window related to the event (e.g. by window which is created to the
    workspace or by window which is moved into it). Note that this changes the name even when moving windows
    *inside* the workspace. TODO: Add fix for this or introduce it as another mode after figuring out the best behavior
    FIRST_WINDOW: Workspace is named after the window which happens to be first in the workspace's tree hierarchy.
    """
    LATEST_WINDOW = 1
    FIRST_WINDOW = 2


rename_rule = RenameRule.FIRST_WINDOW

# Workspaces which have dynamically changing icons.
dynamic_workspace_names = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
