import bpy

from ..utils import Path

class C_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.helloworld"
    bl_label = "Hello World"

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        print("hello world :)")
        print(repr(Path.get_blenderfile_path()))
        print(repr(Path.get_blenderfile_dirname()))
        print(repr(Path.get_addon_dirname()))
        print(repr(Path.get_assets_dirname()))
        print(repr(Path.get_temp_dirname()))
        return {'FINISHED'}
    
    

    