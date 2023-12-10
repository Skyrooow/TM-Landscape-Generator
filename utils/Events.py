"""On_active_obj, on_startup & on_save routines"""

import bpy
from bpy.app.handlers import persistent

from . import Path
from . import Log




# logging
log = Log.get_logger(__name__)


# Object that will store the handle to the msgbus subscription
active_obj_handle_owner = object()


# On active object change, run each time an object is selected in the outliner
# or if active object change in viewport
def on_active_obj(*args) -> None:
    """Run when active object is changed"""
    log.info(f"Active object is: {bpy.context.object.name}, type: {bpy.context.object.type}")


# Add subscriber to 'active object' msgbus 
@persistent
def subscribe_active_obj(dummy) -> None:
    """Subscribe to active object update"""
    bpy.msgbus.clear_by_owner(active_obj_handle_owner)
    bpy.msgbus.subscribe_rna(
            key=(bpy.types.LayerObjects, "active"),
            owner=active_obj_handle_owner,
            args=(),
            notify=on_active_obj,
            options={"PERSISTENT"}
        )


# Remove any subscriber from msgbus
@persistent
def unsubscribe_active_obj(dummy) -> None:
    bpy.msgbus.clear_by_owner(active_obj_handle_owner)


# Do stuff after blender startup
@persistent
def on_load_post(filepath) -> None:
    """Run post blender startup & file load"""
    filepath = Path.native_path(filepath)
    if filepath == "":
        # Run post startup
        log.info("EVENT: post startup")
    else:
        # Run post file load
        log.info("EVENT: post file load")


# Do stuff after blender file save
@persistent
def on_save_post(filepath)-> None:
    """Run post blender file save"""
    log.info("EVENT: post save")
    

# Load event handlers
def load_handlers() -> None:
    """Load message subscriber, startup & save routines"""
    subscribe_active_obj(active_obj_handle_owner)

    if subscribe_active_obj not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(subscribe_active_obj)
        
    if on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_load_post)

    if on_save_post not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(on_save_post)


# Delete event handlers
def delete_handlers() -> None:
    """remove message subscriber, startup & save routines"""
    unsubscribe_active_obj(active_obj_handle_owner)

    if subscribe_active_obj in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(subscribe_active_obj)
        
    if on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_load_post)

    if on_save_post in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(on_save_post)