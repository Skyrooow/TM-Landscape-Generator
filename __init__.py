bl_info = {
    "name": "TM Landscape Generator",
    "author": "Skyrow",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "3D viewport > Sidebar > TM Landscape",
    "description": "",
    "category": "Trackmania",
}

ROOT_PATH = __file__
LOG_DEBUG = False

import bpy

from . import properties
from . import operators
from . import panels
from .utils import events
from .utils import logs


# register addon
def register():
    logs.start_logging()

    # Register classes
    properties.register_classes()
    operators.register_classes()
    panels.register_classes()

    events.start_listening()

# unregister addon
def unregister():
    events.stop_listening()

    # Unregister classes
    panels.unregister_classes()
    operators.unregister_classes()
    properties.unregister_classes()

    logs.stop_logging()