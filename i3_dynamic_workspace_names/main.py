from i3ipc import Connection, Event

from i3_dynamic_workspace_names.configuration import dynamic_workspace_names, rename_rule, RenameRule


def start():
    i3 = Connection()

    def _allow_dynamic_change(ws):
        return ws.num in dynamic_workspace_names

    def _on_ws_change(self, e):
        if e.current:
            workspace = e.current
            update_workspace_name(workspace)

    def _on_window_move(self, e):
        target_ws = i3.get_tree().find_by_id(e.container.id).workspace()
        _rename_workspace(target_ws, e.container.window_class)

    def _on_window_change(self, e):
        visible_workspaces = [ws for ws in i3.get_workspaces() if ws.focused is True]
        focused_window = i3.get_tree().find_focused()
        for ws in visible_workspaces:
            if e.ipc_data['change'] == 'new':
                _rename_workspace(ws, e.ipc_data['container']['window_properties']['class'])
            elif e.ipc_data['change'] == 'close':
                if focused_window is None:
                    return

                if focused_window.type == 'workspace':
                    # The window was the last one open and workspace is empty
                    _rename_workspace(ws, 'empty')
                else:
                    # The other window is still open so use it to set the workspace name
                    _rename_workspace(ws, focused_window.window_class)

    def _rename_workspace(workspace, related_window_class):
        if rename_rule == RenameRule.LATEST_WINDOW:
            window_class_to_use = related_window_class
        elif rename_rule == RenameRule.FIRST_WINDOW:
            window_class_to_use = related_window_class
            ws_container_tree = i3.get_tree().find_named(workspace.name)
            first_window = _find_first_container_with_class(ws_container_tree[0])
            if first_window is not None:
                window_class_to_use = first_window.window_class

        if _allow_dynamic_change(workspace):
            ws_name = "%s:%s" % (workspace.num, window_class_to_use)
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

    # Define a callback to be called when you switch workspaces.
    def update_workspace_name(workspace):
        leaves = workspace.leaves()
        if len(leaves) > 0:
            focused = leaves[0]
            _rename_workspace(focused.workspace(), focused.window_class)

    # Dynamically name your workspaces after the current window class
    def on_window_focus(i3, e):
        focused = i3.get_tree().find_focused()
        ws_name = "%s:%s" % (focused.workspace().num, focused.window_class.lower())
        i3.command('rename workspace to "%s"' % ws_name)

    # Subscribe to events
    # i3.on(Event.WORKSPACE_FOCUS, _on_ws_change)
    i3.on(Event.WINDOW_NEW, _on_window_change)
    i3.on(Event.WINDOW_CLOSE, _on_window_change)
    i3.on(Event.WINDOW_MOVE, _on_window_move)
    # i3.on(Event.WINDOW_FOCUS, on_window_focus)

    # Start the main loop and wait for events to come in.
    i3.main()


if __name__ == '__main__':
    start()
