import bpy

from . import _MainPanel
from .. import bl_info
from ..utils.constants import (
    GIT_REPO_URL,
)
from ..utils.logs import html_logs_filepath
from ..utils.update import AddonUpdate
from ..operators import (
    UI_OT_open_url,
    TMLG_OT_update_check,
    TMLG_OT_update_download,
)

class VIEW3D_PT_lanscape_gen(_MainPanel, bpy.types.Panel):
    bl_label = "TM Landscape Generator"

    def draw_header(self, context):
        pass

    def draw(self, context):
        current_version_str = f'v{".".join(str(i) for i in bl_info["version"])}'
        new_version_str = f'v{".".join(str(i) for i in AddonUpdate.latest_addon_version)}'
        
        layout = self.layout      
        row = layout.row(align=True)
        if AddonUpdate.update_successful:
            row.label(text='Blender must be restarted !', icon ='FILE_SCRIPT')
        else:
            row.label(text=f'{current_version_str}', icon='FILE_SCRIPT')
            if AddonUpdate.can_update:
                row.alert = True
                row.operator(TMLG_OT_update_download.bl_idname, text=f'{new_version_str}', icon='IMPORT')
                row.alert = False
            else:
                row.operator(TMLG_OT_update_check.bl_idname, text='', icon='FILE_REFRESH')
        
        row.operator(UI_OT_open_url.bl_idname, text='', icon='URL').url = GIT_REPO_URL
        row.operator(UI_OT_open_url.bl_idname, text='', icon='FILE_TEXT').url = str(html_logs_filepath)