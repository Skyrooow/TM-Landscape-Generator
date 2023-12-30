import textwrap
import bpy

from ..utils import path
from ..utils import logs

log = logs.get_logger(__name__)

library_parent = '_TM_ProceduralScenery'
library_name = 'TM_ProceduralScenery.blend'
blend_FilePath = str(path.make_path(__file__).parent / library_parent / library_name)


def lib_exists() -> bool:
    return library_name in bpy.data.libraries


def are_all_assets_loaded() -> bool:
    all_loaded = True

    if lib_exists:
        with bpy.data.libraries.load(blend_FilePath, link=True, assets_only=True) as (data_from, data_to):
            data_from: bpy.types.BlendData
            data_to: bpy.types.BlendData
        
            for attr in dir(data_to):
                if attr == "node_groups":
                    for ID in getattr(data_from, attr):
                        if ID not in getattr(data_to, attr) or ID not in getattr(bpy.data, attr):
                            all_loaded = False
    else:
        all_loaded = False
    
    return all_loaded


def load_assets() -> bpy.types.BlendData:
    log.info(textwrap.dedent(f'\
                             Loading assets...\n\
                               from "{blend_FilePath}"')
    )

    with bpy.data.libraries.load(blend_FilePath, link=True, assets_only=True) as (data_from, data_to):
        data_from: bpy.types.BlendData
        data_to: bpy.types.BlendData
        
        for attr in dir(data_to):
            if attr == "node_groups":
                IDs = [
                    name for name in getattr(data_from, attr) if(name.startswith("TM_")
                                                                    & (name not in getattr(bpy.data, attr)))
                ]
                if len(IDs) > 0:
                    IDs_string = "\n- ".join(IDs)
                    log.debug(f'{attr}:\n- {IDs_string}')
                    setattr(data_to, attr, IDs)
    
    log.info('Finished !')
    return data_to