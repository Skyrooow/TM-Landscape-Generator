import bpy
import os

from .. import ADDON_DIRNAME

def native_path(path: str) -> str:
    return bpy.path.native_pathsep(path)


def is_path_existing(pathname: str) -> bool:
    return os.path.exists(pathname)


def dirname(pathname: str) -> str:
    return os.path.dirname(pathname)


# return "" if file not saved on drive
def get_blenderfile_dirname() -> str:
    filepath = native_path(bpy.data.filepath)
    return dirname(filepath)


def get_addon_dirname() -> str:
    return ADDON_DIRNAME


def get_assets_dirname() -> str:
    return os.path.join(ADDON_DIRNAME, 'assets')


def get_app_tempdir() -> str:
    return native_path(bpy.app.tempdir)

