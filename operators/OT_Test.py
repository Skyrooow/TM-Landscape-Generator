import bpy
import sys

from ..utils import Log


# Logging
log = Log.getLogger(__name__)


class C_OT_Test(bpy.types.Operator):
    bl_idname = "view3d.test"
    bl_label = "Test"

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        log.info("User pressed the Test button !")

        try:
            speed = self.somefunc(4.2, 0.)
            log.info(str(speed))
        except:
            log.exception("Something went wrong...")

        return {'FINISHED'}
    
    
    @classmethod
    def anotherfunc(cls, a: float, b: float) -> float:
        result = 0.
        result = a / b
        return result
    
    @classmethod
    def somefunc(cls, dist: float, time: float) -> str:
        return cls.anotherfunc(dist, time)