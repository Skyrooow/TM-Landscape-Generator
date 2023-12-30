"""Expose panel subclasses and (un)register function."""


class _MainPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TM Landscape'


class _ChildPanel(_MainPanel):
    bl_parent_id = 'VIEW3D_PT_lanscape_gen'


from .PT_landscape_gen import (
    VIEW3D_PT_lanscape_gen,
)

from .PT_configuration import (
    VIEW3D_PT_test,
)


_classes = (
    # Register order is important for panels :
    # - Parents must be registered before childs
    # - Panels registered first will appear above other panels
    VIEW3D_PT_lanscape_gen,
    VIEW3D_PT_test,
)

def register_classes():
    import bpy
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    import bpy
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)