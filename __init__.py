# Import builtin modules
import bpy
import os

# Addon directory name
ADDON_DIRNAME = os.path.dirname(__file__)

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

# import addon modules
from .utils.Path                    import *

# import classes
from .operators.OT_HelloWorld       import *

from .panels.PT_HelloWorld          import *


# register classes
classes = (
    SK_OT_HelloWorld,
    SK_PT_HelloWorld,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        #print(" ".join(("-Registered:", str(cls))))

    #print(" ".join(("Addon loaded:", get_addon_dirname())))


# unregister classes
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)