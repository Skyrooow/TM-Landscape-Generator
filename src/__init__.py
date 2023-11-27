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
from bpy.utils import *


# import classes
from .operators.OT_HelloWorld     import *
from .panels.PT_HelloWorld        import *

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
    
