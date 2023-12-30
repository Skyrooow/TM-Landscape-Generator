import bpy

from ... import bl_info
from ...utils.update import AddonUpdate


class TMLG_OT_update_check(bpy.types.Operator):
    """Check if new release is available"""
    bl_idname = 'tmlg.update_check'
    bl_label = 'Check Update'

    def execute(self, context):
        AddonUpdate.check_for_new_release()

        if AddonUpdate.can_update:
            self.report({'INFO'}, f'{bl_info["name"]}: update available !')
        elif AddonUpdate.new_addon_available and not AddonUpdate.current_blender_supported:
            self.report({'ERROR'}, f'A new version is available but blender version is too old ! Minimal is {AddonUpdate.latest_minimal_blender_version}).')
        else:
            self.report({'INFO'}, f'{bl_info["name"]}: no update available.')

        if context.area:
            context.area.tag_redraw()
            
        return {'FINISHED'}        

