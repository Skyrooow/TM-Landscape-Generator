import bpy

from ..utils.Constants import BasePanel



class C_PT_HelloWorld(BasePanel, bpy.types.Panel):
    # idname = class name
    bl_label = "Hello World"


    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("view3d.helloworld")
        