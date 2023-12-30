import bpy

from ... import assets


class TMLG_OT_import_assets(bpy.types.Operator):
    bl_idname = 'tmlg.import_assets'
    bl_label = 'Import Assets'

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        self.report({'INFO'}, f'{assets.blend_FilePath = }')

        lib_exists = assets.lib_exists()
        self.report({'INFO'}, f'{lib_exists = }')

        all_loaded = assets.are_all_assets_loaded()
        self.report({'INFO'}, f'{all_loaded = }')

        assets.load_assets()

        return {'FINISHED'}