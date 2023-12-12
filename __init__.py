"""
Blender addon for Trackmania2020


"""


bl_info = {
    "name": "TM Scenery Addon",
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


import os
import bpy

ADDON_DIRNAME = os.path.dirname(__file__)
"""Main __init__.py directory"""

from .utils import Events
from .utils import Log


# import bpy classes
from .operators.OT_HelloWorld       import C_OT_HelloWorld
from .operators.OT_Test             import C_OT_Test

from .panels.PT_HelloWorld          import C_PT_HelloWorld
from .panels.PT_Test                import C_PT_Test


# classes register list (order matters for panels)
classes = (
    # Properties

    # Operators
    C_OT_HelloWorld,
    C_OT_Test,

    # Panels
    C_PT_HelloWorld,
    C_PT_Test,
)




# Logger
log = Log.getLogger(__name__)


# register addon
def register():
    Log.start()

    for cls in classes:
        bpy.utils.register_class(cls)

    Events.start_listening()


# unregister addon
def unregister():
    Events.stop_listening()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    Log.stop()