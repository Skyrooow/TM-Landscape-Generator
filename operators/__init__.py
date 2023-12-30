"""Expose operator subclasses and (un)register function."""


# trackmania landscape generator 
from .tmlg.OT_import_assets import (
    TMLG_OT_import_assets,
)
from .tmlg.OT_update_check import (
    TMLG_OT_update_check,
)
from .tmlg.OT_update_download import (
    TMLG_OT_update_download,
)

# ui
from .ui.OT_message_popup import (
    UI_OT_message_popup,
)
from .ui.OT_open_url import (
    UI_OT_open_url,
)


_classes = (
    TMLG_OT_import_assets,
    TMLG_OT_update_check,
    TMLG_OT_update_download,
    UI_OT_message_popup,
    UI_OT_open_url,
)

def register_classes():
    import bpy
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    import bpy
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)