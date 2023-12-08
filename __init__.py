# Import builtin modules
import bpy
import os



# Addon directory name
ADDON_DIRNAME = os.path.dirname(__file__)
"""Main __init__.py directory"""



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



# import my modules
from .utils import Handlers
from .utils import Log

# Logger declaration
log = Log.get_master_logger(__name__, debug=True)



# import my classes
from .operators.OT_HelloWorld       import C_OT_HelloWorld
from .operators.OT_Test             import C_OT_Test

from .panels.PT_HelloWorld          import C_PT_HelloWorld
from .panels.PT_Test                import C_PT_Test

# classes register order
classes = (
    # Properties

    # Operators
    C_OT_HelloWorld,
    C_OT_Test,

    # Panels
    C_PT_HelloWorld,
    C_PT_Test,
)



# regiser addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Handlers.load_handlers()

    log.info(f"{__name__} registered")
    


# unregister addon
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    Handlers.delete_handlers()

    log.info(f"{__name__} unregistered")    