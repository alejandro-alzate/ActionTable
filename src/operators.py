import bpy
from .exporter import export_to_lua


class LE_OP_add_path(bpy.types.Operator):
    bl_idname = "lua_export.add_path"
    bl_label = "Add action"

    def execute(self, context):
        settings = context.scene.le_settings
        obj = context.object
        act = None

        if obj:
            ad = getattr(obj, 'animation_data', None)
            if ad:
                act = getattr(ad, 'action', None)
                if not act:
                    for t in getattr(ad, 'nla_tracks', []):
                        for s in getattr(t, 'strips', []):
                            if getattr(s, 'action', None):
                                act = s.action
                                break
                        if act:
                            break

        if not act:
            self.report({'INFO'}, 'Active object has no action')
            print('[LuaExport] Add failed: active object has no action')
            return {'CANCELLED'}

        for p in settings.paths:
            if p.action == act:
                self.report({'INFO'}, f"Action '{act.name}' already in list")
                print(f"[LuaExport] Add skipped: '{act.name}' already in list")
                return {'CANCELLED'}

        item = settings.paths.add()
        item.action = act
        settings.active_index = len(settings.paths) - 1

        print(f"[LuaExport] Added action: {act.name}")
        for fc in getattr(act, 'fcurves', []):
            print(f"[LuaExport]   {act.name}: {fc.data_path}[{fc.array_index}]")

        self.report({'INFO'}, f"Added action: {act.name}")
        return {'FINISHED'}


class LE_OP_remove_path(bpy.types.Operator):
    bl_idname = "lua_export.remove_path"
    bl_label = "Remove action"

    def execute(self, context):
        settings = context.scene.le_settings
        idx = settings.active_index

        if settings.paths and 0 <= idx < len(settings.paths):
            name = settings.paths[idx].action.name if settings.paths[idx].action else '<No Action>'
            settings.paths.remove(idx)

            if settings.paths:
                settings.active_index = min(idx, len(settings.paths) - 1)
                self.report({'INFO'}, f"Removed: {name}")
                print(f"[LuaExport] Removed: {name}")
            else:
                settings.active_index = 0
                self.report({'INFO'}, 'There no more actions to remove')
                print('[LuaExport] There no more actions to remove')

            return {'FINISHED'}

        self.report({'INFO'}, 'There no more actions to remove')
        print('[LuaExport] Remove failed: no actions to remove')
        return {'CANCELLED'}


class LE_OP_autofill(bpy.types.Operator):
    bl_idname = "lua_export.autofill"
    bl_label = "Autofill with all actions"

    def execute(self, context):
        settings = context.scene.le_settings
        settings.paths.clear()
        found = [act for act in bpy.data.actions if getattr(act, 'fcurves', None) and len(act.fcurves) > 0]

        for act in found:
            item = settings.paths.add()
            item.action = act

        settings.active_index = 0 if settings.paths else 0
        self.report({'INFO'}, f"Found {len(found)} actions across all objects")
        print(f"[LuaExport] Autofill found {len(found)} actions")
        return {'FINISHED'}


class LE_OP_export_to_lua(bpy.types.Operator):
    bl_idname = "lua_export.export_to_lua"
    bl_label = "Export to Lua"

    def execute(self, context):
        settings = context.scene.le_settings
        if settings.global_search:
            actions = list(bpy.data.actions)
        else:
            actions = [p.action for p in settings.paths if p.action]

        if not actions:
            self.report({'WARNING'}, 'No actions selected to export')
            print('[LuaExport] Export cancelled: no actions')
            return {'CANCELLED'}

        path = bpy.path.abspath(settings.export_path)
        export_to_lua(filepath=path, use_seconds=True, actions=actions)

        self.report({'INFO'}, f"Exported {len(actions)} actions to {path}")
        print(f"[LuaExport] Exported {len(actions)} actions to {path}")
        return {'FINISHED'}


# proper registration
classes = (
    LE_OP_add_path,
    LE_OP_remove_path,
    LE_OP_autofill,
    LE_OP_export_to_lua,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
