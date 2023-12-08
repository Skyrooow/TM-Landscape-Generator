"""Functions relative to handling path variables and retrieving common path for the addon."""

import bpy
import os

from .. import ADDON_DIRNAME


def native_path(path: str) -> str:
    """Returns the path with system native separators."""
    return bpy.path.native_pathsep(path)


def is_path_existing(pathname: str) -> bool:
    """Test whether a path exists. Returns False for broken symbolic links."""
    return os.path.exists(pathname)


def join(path:str, *paths:str) -> str:
    return os.path.join(path, *paths)


def dirname(pathname: str) -> str:
    """Returns the directory component of a pathname."""
    return os.path.dirname(pathname)


def get_addon_dirname() -> str:
    """Returns the addon directory."""
    return ADDON_DIRNAME


def get_assets_dirname() -> str:
    """Returns the addon assets directory."""
    return join(get_addon_dirname(), 'assets')


def get_logfile_path() -> str:
    """Return the log file path"""
    return join(get_addon_dirname(), 'log.txt')


def get_blenderfile_path() -> str:
    """Returns full path to the current blender file. Empty string if not exists."""
    return native_path(bpy.data.filepath)


def get_blenderfile_dirname() -> str:
    """Returns current blender file directory. Empty string if file not exists."""
    return dirname(get_blenderfile_path())