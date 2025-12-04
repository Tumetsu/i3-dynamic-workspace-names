from enum import Enum
import configparser
import json


class RenameRule(Enum):
    """
    The rule about which window is used to rename the workspace when workspace
    rename is triggered.

    FIRST_WINDOW: Workspace is named after the window which happens to be first in the workspace's tree hierarchy.
    TODO: FOCUSED_WINDOW might make sense as an alternative at least when the workspace is focused?
    """
    FIRST_WINDOW = 1


class DynamicWorkspaceNamesConfig:
    def __init__(self, rename_rule, dynamic_workspace_names):
        self.rename_rule = rename_rule
        self.dynamic_workspace_names = dynamic_workspace_names


def load_configuration_file(path):
    if path is None:
        return DynamicWorkspaceNamesConfig(rename_rule_default, dynamic_workspace_names_default)

    config = configparser.ConfigParser()
    config.read(path)
    behavior = config['Behavior']

    return DynamicWorkspaceNamesConfig(rename_rule_default, json.loads(behavior['DynamicWorkspaceIndexes']))


# Default settings
rename_rule_default = RenameRule.FIRST_WINDOW
dynamic_workspace_names_default = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
