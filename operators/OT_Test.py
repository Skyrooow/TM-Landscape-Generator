import bpy

from ..utils import logs

from ..assets import blend

# Logging
log = logs.get_logger(__name__)


class C_OT_Test(bpy.types.Operator):
    bl_idname = "view3d.test"
    bl_label = "Test"

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        log.info("User pressed the Test button !")

        try:
            blend.load_assets()
        except:
            log.exception("Something went wrong...")

        return {'FINISHED'}
    
  