import bpy


class LE_PG_OutputPath(bpy.types.PropertyGroup):
    action: bpy.props.PointerProperty(
        name="Action",
        type=bpy.types.Action,
    )


class LE_PG_OutputSettings(bpy.types.PropertyGroup):
    paths: bpy.props.CollectionProperty(type=LE_PG_OutputPath)
    active_index: bpy.props.IntProperty(default=0)
    global_search: bpy.props.BoolProperty(
        name="Global",
        description="Export all actions instead of just the listed ones",
        default=False,
    )
    export_path: bpy.props.StringProperty(
        name="Output File",
        description="Where to export the Lua file",
        subtype="FILE_PATH",
        default="//anim.lua",
    )


classes = (
    LE_PG_OutputPath,
    LE_PG_OutputSettings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.le_settings = bpy.props.PointerProperty(type=LE_PG_OutputSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.le_settings
