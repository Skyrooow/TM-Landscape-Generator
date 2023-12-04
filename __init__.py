# Blender addon info
bl_info = {
    "name": "TM Scenery Tools",
    "author": "Skyrow",
    "version": (0, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View",
}

# Import builtin modules
import bpy
import os


# Addon directory name
ADDON_DIRNAME = os.path.dirname(__file__)
"""Main __init__.py directory"""


# import my modules
from .utils import Handlers

# import my classes
from .operators.OT_HelloWorld       import C_OT_HelloWorld

from .panels.PT_HelloWorld          import C_PT_HelloWorld
from .panels.PT_WhereAmII           import C_PT_WhereAmI
from .panels.PT_zzz                 import C_PT_zzz


# classes register order
classes = (
    # Properties

    # Operators
    C_OT_HelloWorld,

    # Panels
    C_PT_HelloWorld,
    C_PT_WhereAmI,
    C_PT_zzz,
)


# regiser addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Handlers.load_handlers()


# unregister addon
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    Handlers.delete_handlers()