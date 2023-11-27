# define blender addon info
bl_info = {
    "name": "Undefined",
    "author": "Skyrow",
    "version": (0, 0, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View",
}


# Import blender modules
import bpy


# import classes
class SK_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.hello_world"
    bl_label = "Hello World"
    
    def execute(self, context):
        print("hello world")
        return {'FINISHED'}

class SK_PT_HelloWorld(bpy.types.Panel):
    bl_idname = "SK_PT_HelloWorld"
    bl_label = "Hello World"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("view3d.hello_world")


# register classes
classes = (
    SK_OT_HelloWorld,
    SK_PT_HelloWorld,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# run register() if file is executed
if __name__ == "__main__":
    register()
    
