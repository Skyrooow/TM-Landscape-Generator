import bpy
import webbrowser


class UI_OT_open_url(bpy.types.Operator):
    """Open an url or a local file in the web browser"""
    bl_idname = "ui.open_url"
    bl_label = "Open URL"

    url: bpy.props.StringProperty("")
        
    def execute(self, context):
        webbrowser.open(self.url)
        return {"FINISHED"}
    
    @classmethod
    def description(cls, context, properties) -> str:
        return f'"{properties.url}"'