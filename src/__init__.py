bl_info = {
    "name": "ActionTables",
    "author": "Alejandro Alzate",
    "version": (0, 1, 0),
    "blender": (4, 4, 3),
    "location": "View3D > Sidebar > Lua Export",
    "description": "Export keyframes to a Lua file",
    "category": "Animation",
}

import importlib
import bpy

# Import local modules
from . import properties, operators, ui, exporter


modules = (
    properties,
    operators,
    ui,
    exporter,
)


def register():
    for m in modules:
        importlib.reload(m)
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
