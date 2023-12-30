"""Functions relative to handling path variables and retrieving common path for the addon."""

import bpy
from pathlib import Path

from .. import ROOT_PATH


def make_path(*args: str) -> Path:
    """Returns the given string(s) as Path object"""
    return Path(*args)


def get_addon_path() -> Path:
    """Returns the addon path."""
    return make_path(ROOT_PATH).parent


def get_blenderfile_path() -> Path:
    """Returns full path to the current blender file. Empty string if not exists."""
    return make_path(bpy.data.filepath)


def get_assets_dirname() -> str:
    """Returns the addon assets directory."""
    return make_path(get_addon_path(), 'assets')