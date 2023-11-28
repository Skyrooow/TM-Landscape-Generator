import bpy


class SK_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.helloworld"
    bl_label = "OT_HelloWorld"


    def execute(self, context):
        print("hello world")
        return {'FINISHED'}
    