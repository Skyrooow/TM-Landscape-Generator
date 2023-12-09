"""\
Blender addon for Trackmania2020
Author : Skyrow
"""

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


# Import built-in modules
import bpy
import os


LOG_DEBUG = True
"""Toggle debug log level"""

ADDON_DIRNAME = os.path.dirname(__file__)
"""Main __init__.py directory"""


# import third-party modules
from .utils import Events
from .utils import Log


# import bpy classes
from .operators.OT_HelloWorld       import C_OT_HelloWorld
from .operators.OT_Test             import C_OT_Test

from .panels.PT_HelloWorld          import C_PT_HelloWorld
from .panels.PT_Test                import C_PT_Test


# classes register list (order matters in panels)
classes = (
    # Properties

    # Operators
    C_OT_HelloWorld,
    C_OT_Test,

    # Panels
    C_PT_HelloWorld,
    C_PT_Test,
)




# Logging
log = Log.get_logger(__name__)


# regiser addon
def register():
    Log.start()
    log.info(f"{__name__} register start...")

    # register bpy classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # load event handlers
    Events.load_handlers()

    log.info(f"{__name__} registered !")



# unregister addon
def unregister():
    log.info(f"{__name__} unregister start...")

    # register bpy classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # remove event handlers
    Events.delete_handlers()

    log.info(f"{__name__} unregistered !")
    Log.stop()