import bpy



class C_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.helloworld"
    bl_label = "Hello World"

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        print("hello world :)")
        return {'FINISHED'}
    
    

    