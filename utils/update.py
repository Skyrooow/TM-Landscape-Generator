"""Automatic detection of new release and update function encapsuled in a single class.

### Mandatory for a new release:
- Tag name must contain the version number formatted as:
  - "v%d.%d.%d" <=> "v<major>.<minor>.<patch>" (addon version)

- Asset file must always end with:
  - "%d.%d.zip" <=> "<major>.<minor>.zip" (blender version)
"""

import bpy
import shutil
import requests
import zipfile
import re
import io

from .. import bl_info
from ..utils import path
from ..utils import logs
from ..utils.constants import (
    URL_RELEASES,
)

log = logs.get_logger(__name__)


class AddonUpdate():   
    current_addon_version:tuple = bl_info["version"]
    current_blender_version:tuple = bpy.app.version
    latest_addon_version:tuple = (0,0,0)
    latest_minimal_blender_version:tuple = (0,0,0)
    latest_is_prerelease:bool = False
    latest_filename:str = None
    latest_download_url:str = None
    
    new_addon_available:bool = False
    current_blender_supported:bool = False
    can_update: bool = False
    update_successful = False

    @classmethod
    def check_can_update(cls) :
        cls.new_addon_available = cls.latest_addon_version > cls.current_addon_version
        cls.current_blender_supported = cls.current_blender_version > cls.latest_minimal_blender_version

        log.debug(f'Addon current -> latest : {cls.current_addon_version} -> {cls.latest_addon_version}')
        log.debug(f'Blender current -> minimal : {cls.current_blender_version} -> {cls.latest_minimal_blender_version}')
        log.debug(f'{cls.latest_is_prerelease = }')

        if cls.new_addon_available:
            log.info(f'Update available: v{cls.latest_addon_version} > {cls.current_addon_version}')
            if cls.current_blender_supported:
                cls.can_update = True
            else:
                cls.can_update = False
                log.error(f'Current blender {cls.current_blender_version} isn\'t supported ! Minimal is {cls.latest_minimal_blender_version}')
        else:
            cls.can_update = False
            log.info('No update available')


    @classmethod
    def check_for_new_release(cls):
        log.info('Checking for new release...')
        try:
            response = requests.get(URL_RELEASES)
            # Parse latest release
            latest = response.json()[0]
            latest_tag_name    = latest['tag_name']
            latest_is_prerelease = latest['prerelease']
            latest_asset = latest['assets'][0]
            latest_asset_name = latest_asset['name']
            latest_asset_download_url = latest_asset['browser_download_url']
            # Get latest addon version from github API      
            pattern = rf'^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
            match = re.search(pattern, latest_tag_name, flags=re.IGNORECASE)
            latest_addon_version = (int(match.group('major')), int(match.group('minor')), int(match.group('patch')))
            # Get latest addon blender version from the asset name
            pattern = rf'(?P<major>\d+)\.(?P<minor>\d+)\.zip$'
            match = re.search(pattern, latest_asset_name, flags=re.IGNORECASE)
            latest_minimal_blender_version = (int(match.group('major')), int(match.group('minor')))
        except Exception as e:
            log.exception('Error during parse of release metadata.')
        else:
            # Update class attributes
            cls.latest_addon_version = latest_addon_version
            cls.latest_is_prerelease = latest_is_prerelease
            cls.latest_minimal_blender_version = latest_minimal_blender_version
            cls.latest_filename = latest_asset_name
            cls.latest_download_url = latest_asset_download_url        
        finally:
            cls.check_can_update()


    @classmethod
    def do_update(cls) -> None:
        
        def on_rmtree_error(function, path, excinfo):
            log.error(f'<{function.__name__}> {excinfo[1]}')

        if cls.can_update:
            log.info('Updating addon now...')

            url = cls.latest_download_url
            addon_path = path.get_addon_path().resolve()
            extract_to = addon_path.parent

            log.debug(f'{addon_path = }')
            log.debug(f'{extract_to = }')
            
            try:
                r = requests.get(url)
                z = zipfile.ZipFile(io.BytesIO(r.content))

                shutil.rmtree(addon_path, ignore_errors=False, onerror=on_rmtree_error)
                z.extractall(extract_to)
                
            except Exception as e:
                log.exception('Error during addon update')

            else:
                cls.update_successful = True
                log.info('Addon updated, blender must be restarted.')