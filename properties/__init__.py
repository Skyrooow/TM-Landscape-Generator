"""Expose property subclasses and (un)register function."""

# Private

# Public
from .preferences import TMLG_Prefs
from .properties import TMLG_Props


_classes = (
    TMLG_Prefs,
    TMLG_Props,
)

def register_classes():
    import bpy
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    import bpy
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
