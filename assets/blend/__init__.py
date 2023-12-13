import bpy

from ...utils import path
from ...utils import logs

log = logs.get_logger(__name__)

blendFilePath = path.join(path.dirname(__file__), 'TM_ProceduralScenery.blend')

def load_assets():
    log.debug('Load assets from %s' % blendFilePath)
    with bpy.data.libraries.load(blendFilePath, link=True, assets_only=True) as (data_from, data_to):
        data_from:bpy.types.BlendData
        data_to:bpy.types.BlendData
            
        data_to.node_groups = [name for name in data_from.node_groups if name.startswith("TM_") & (name not in data_to.node_groups) & (name not in bpy.data.node_groups)]

        
