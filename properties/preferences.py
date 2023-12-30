import bpy

from .. import bl_info


class TMLG_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    do_check_new_release_on_startup: bpy.props.BoolProperty(
        name='Check For New Release On Startup',
        description='Check for a new addon release everytime blender startups.',
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text=f'{bl_info["name"]} preferences.')
        col = layout.column(align=True)
        col.prop(self, 'do_check_new_release_on_startup')