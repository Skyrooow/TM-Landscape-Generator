import bpy

from ..utils import Path

# Logger declaration
from ..utils import Log
log = Log.get_logger(__name__)


class C_OT_HelloWorld(bpy.types.Operator):
    bl_idname = "view3d.helloworld"
    bl_label = "Hello World"

    @classmethod
    def poll(cls, context) -> bool:
        return True #no specific context restriction

    def execute(self, context):
        log.info("User pressed the HelloWorld button !")
        return {'FINISHED'}
    
    

    