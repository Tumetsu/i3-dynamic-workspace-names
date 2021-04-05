# Dynamic i3 workspace names

This Python script listens i3 ipc messages and 
dynamically changes the names of the workspaces
to the lowercase variant of one window in the workspace prefixed by
workspace index.
For example by moving Gnome terminal to the workspace `7` the workspace
will be renamed to `7:gnome-terminal`

This functionality can then be used e.g. in Polybar
to display custom icons for workspaces based on opened
apps with following sample config for Polybar i3 module:

```
[module/i3]
< rest of i3 module the config here >

fuzzy-match = true
ws-icon-0 = 1;
ws-icon-1 = 2;
ws-icon-2 = 3;
ws-icon-3 = 4;
ws-icon-4 = 5;
ws-icon-5 = 6;
ws-icon-6 = jetbrains;
ws-icon-7 = firefox;
ws-icon-8 = terminal;
ws-icon-9 = telegram;
ws-icon-10 = spotify;
ws-icon-11 = nautilus;
ws-icon-12 = vim;
ws-icon-13 = sublime;
ws-icon-14 = chrome;
ws-icon-15 = chromium;
ws-icon-16 = slack;
ws-icon-17 = 10;
ws-icon-default = 
```

## Install
Clone the repository and in root run:
```
pip3 install .
```

## How to run
The script can be run manually by
```
i3-dynamic-workspace-names
```

but preferably you should add the following to your i3 
config:
```
exec_always --no-startup-id i3-dynamic-workspace-names
```

## Configuration
You can define the indexes of workspaces which should be dynamically 
renamed by editing the list in the main.py:
```
    _dynamic_workspace_names = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
```
To apply changes, run 
```
pip3 install .
```
