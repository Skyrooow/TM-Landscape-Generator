import bpy
from ..utils.Path import *

class SK_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.helloworld"
    bl_label = "OT_HelloWorld"


    def execute(self, context):
        print("hello world")
        print("Blender file dir: " + get_blenderfile_dirname())
        print("Addon dir: " + get_addon_dirname())
        print("assets dir" + get_assets_dirname())
        print("app temp dir: " + get_app_tempdir())
        return {'FINISHED'}
    