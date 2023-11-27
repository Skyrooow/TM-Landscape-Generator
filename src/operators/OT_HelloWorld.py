import bpy


class SK_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.hello_world"
    bl_label = "Hello World"
    
    def execute(self, context):
        print("hello world")
        return {'FINISHED'}