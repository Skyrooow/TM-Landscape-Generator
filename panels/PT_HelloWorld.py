import bpy


class SK_PT_HelloWorld(bpy.types.Panel):
    bl_idname = "SK_PT_HelloWorld"
    bl_label = "PT_HelloWorld"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("view3d.helloworld")
        