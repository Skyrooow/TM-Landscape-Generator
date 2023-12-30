import bpy

from ... import bl_info
from ...utils.update import AddonUpdate


class TMLG_OT_update_download(bpy.types.Operator):
    """Update the addon with the latest release"""
    bl_idname = 'tmlg.update_download'
    bl_label = 'Do Update'

    def invoke(self, context, event):
        return bpy.types.WindowManager.invoke_props_dialog(self)

    def execute(self, context):
        if AddonUpdate.can_update:
            AddonUpdate.do_update()

            if AddonUpdate.update_successful:
                self.report({'INFO'}, f'{bl_info["name"]}: update successful, blender must be restarted.')
            else:
                self.report({'ERROR'}, f'{bl_info["name"]}: update error, try again later. If the problem persists, save logs and contact staff.')

        if context.area:
            context.area.tag_redraw()
                
        return {'FINISHED'}        

    def draw(self, context):
        layout = self.layout
