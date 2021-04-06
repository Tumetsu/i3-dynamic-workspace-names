from i3ipc import Connection, Event
from i3ipc.events import WindowEvent

from i3_dynamic_workspace_names.configuration import RenameRule, DynamicWorkspaceNamesConfig, load_configuration_file


def start(config: DynamicWorkspaceNamesConfig):
    i3 = Connection()

    def _allow_dynamic_change(ws):
        return ws.num in config.dynamic_workspace_names

    def _on_window_move(connection: Connection, e: WindowEvent):
        target_ws = i3.get_tree().find_by_id(e.container.id).workspace()
        _rename_workspace(target_ws)

        # Refresh the active workspace's name too since we could have moved the
        # naming window out of it
        current_workspace = i3.get_tree().find_focused().workspace()
        _rename_workspace(current_workspace)

    def _on_window_change(connection: Connection, e: WindowEvent):
        visible_workspaces = [ws for ws in i3.get_workspaces() if ws.focused is True]
        focused_window = i3.get_tree().find_focused()
        for ws in visible_workspaces:
            if e.change == 'new':
                _rename_workspace(ws)
            elif e.change == 'close':
                if focused_window is None:
                    return

                if focused_window.type == 'workspace':
                    # The window was the last one open and workspace is empty
                    _rename_workspace(ws)
                else:
                    # There is other window still open so use it to set the workspace name
                    _rename_workspace(ws)

    def _rename_workspace(workspace):
        window_class_to_use = 'empty'
        if config.rename_rule == RenameRule.FIRST_WINDOW:
            ws_container_tree = i3.get_tree().find_named(workspace.name)
            first_window = _find_first_container_with_class(ws_container_tree[0])
            if first_window is not None:
                window_class_to_use = first_window.window_class

        if _allow_dynamic_change(workspace):
            ws_name = f'{workspace.num}:{window_class_to_use}'
            i3.command(f'rename workspace "{workspace.name}" to "{ws_name.lower()}"')

    def _find_first_container_with_class(container_tree):
        """
        Note that the "first" in this implementation is the depth first search!
        Figure out later if breadth first search would make more sense or make it configurable...
        """
        for node in container_tree.nodes:
            if node.window_class is not None:
                return node
            else:
                return _find_first_container_with_class(node)
        return None

    # Subscribe to events
    i3.on(Event.WINDOW_NEW, _on_window_change)
    i3.on(Event.WINDOW_CLOSE, _on_window_change)
    i3.on(Event.WINDOW_MOVE, _on_window_move)

    # Start the main loop and wait for events to come in.
    i3.main()


if __name__ == '__main__':
    start(load_configuration_file(None))
