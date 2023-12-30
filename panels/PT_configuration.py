import bpy

from . import _ChildPanel
from ..operators import (
    TMLG_OT_import_assets
)

class VIEW3D_PT_test(_ChildPanel, bpy.types.Panel):
    bl_label = "Test"

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        layout.operator(TMLG_OT_import_assets.bl_idname, icon='LINKED')