import bpy

from . import Panels


class C_PT_HelloWorld(Panels, bpy.types.Panel):
    # idname = class name
    bl_label = "Hello World"


    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("view3d.helloworld")
        