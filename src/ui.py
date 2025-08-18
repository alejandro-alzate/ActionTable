import bpy


class LE_UL_ActionList(bpy.types.UIList):
    """Custom UIList for displaying actions in the export list."""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item.action:
                layout.label(text=item.action.name, icon="ACTION")
            else:
                layout.label(text="<No Action>")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="")


class LE_PT_panel(bpy.types.Panel):
    bl_label = "Export Actions"
    bl_idname = "LE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ActionTables"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.le_settings

        row = layout.row()
        row.prop(settings, "global_search")

        if not settings.global_search:
            layout.label(text="Export List")

            row = layout.row()
            row.template_list(
                "LE_UL_ActionList",
                "lua_paths",
                settings,
                "paths",
                settings,
                "active_index",
                rows=1,  # so the list collapses to 1 row if wanted
            )

            col = row.column(align=True)
            col.operator("lua_export.add_path", icon="ADD", text="")
            col.operator("lua_export.remove_path", icon="REMOVE", text="")

            layout.operator("lua_export.autofill", icon="FILE_REFRESH")

        row = layout.row()
        row.prop(settings, "export_path", text="")
        layout.operator("lua_export.export_to_lua", icon="EXPORT")


classes = (
    LE_UL_ActionList,
    LE_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
