from i3ipc import Connection, Event


def start():
    i3 = Connection()

    # Workspaces which have dynamically changing icons.
    _dynamic_workspace_names = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    def _allow_dynamic_change(ws):
        return ws.num in _dynamic_workspace_names

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

    def _get_current_workspace(container):
        active_window = i3.get_tree().find_by_window(container.id)
        if active_window is not None:
            current_ws = i3.get_tree().find_by_id(container.id).workspace()
        else:
            current_ws = None

        return current_ws

    def _rename_workspace(workspace, window_class):
        if _allow_dynamic_change(workspace):
            ws_name = "%s:%s" % (workspace.num, window_class)
            i3.command(f'rename workspace "{workspace.name}" to "{ws_name.lower()}"')

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
    i3.on(Event.WORKSPACE_FOCUS, _on_ws_change)
    i3.on(Event.WINDOW_NEW, _on_window_change)
    i3.on(Event.WINDOW_CLOSE, _on_window_change)
    i3.on(Event.WINDOW_MOVE, _on_window_move)
    # i3.on(Event.WINDOW_FOCUS, on_window_focus)

    # Start the main loop and wait for events to come in.
    i3.main()


if __name__ == '__main__':
    start()
