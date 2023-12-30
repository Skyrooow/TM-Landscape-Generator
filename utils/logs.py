"""Formatted logging with colors in console & in html file

Function | Use
:---|:---
start_logging() | Start handling log messages
stop_logging()  | Stop handling log messages
get_logger(name)| Return a logger with the specified name

For each file, create a logger object: `log = logs.get_logger(__name__)`

Logging level | Example | Note
:---|:---|:---
DEBUG     | `log.debug("Debug msg")`
INFO      | `log.info("Info msg")`
WARNING   | `log.warning("Warning msg")`
EXCEPTION | `log.exception("Exception msg")` | Inside of Except block only              
ERROR     | `log.error("Error msg", stack_info=True)`
CRITICAL  | `log.critical("Critical msg", stack_info=True)`
"""

import logging
import html
import platform
import textwrap
import copy
import bpy

from . import path
from .. import (
    bl_info,
    LOG_DEBUG,
)


html_logs_filepath = path.get_addon_path() / 'logs.html'

_debug_info={
    'bl_version'    : bpy.app.version_string,
    'addon_version' : '.'.join(str(i) for i in bl_info["version"]),
    'blender_bin'   : bpy.app.binary_path,
    'addon_path'     : path.get_addon_path(),
    'platform'      : platform.platform(),
    'architecture'  : ' - '.join(str(i) for i in platform.architecture()),
    'processor'     : platform.processor(),
    'py_version'    : platform.python_version(),
}

#---------------------------------------------------------------------------
#   Console Formatter classe
#---------------------------------------------------------------------------

class _ConsoleStyleFormatter(logging.Formatter):
    """This is a formatter which add escape codes to the record."""
    level_to_color = {
        logging.DEBUG       :   '1;34', # bright blue
        logging.INFO        :   '1;32', # bright green
        logging.WARNING     :   '1;33', # bright yellow
        logging.ERROR       :   '1;31', # bright red
        logging.CRITICAL    :   '1;35', # bright magenta   
    }

    def format(self, record) -> str:
        # Do not edit the original record, this let multiple formatters handling the same record 
        cpyRecord = copy.copy(record) 

        levelcolor = self.level_to_color[cpyRecord.levelno]
        
        cpyRecord.levelname     = f'\x1b[{levelcolor}m{cpyRecord.levelname:^9}\x1b[0m'
        cpyRecord.name          = f'\x1b[{levelcolor}m{cpyRecord.name}\x1b[0m'
        cpyRecord.threadName    = f'\x1b[{levelcolor}m{cpyRecord.threadName}\x1b[0m'
        cpyRecord.msg           = f'\x1b[2m{cpyRecord.msg}\x1b[0m' # faint
        return super().format(cpyRecord)

    def formatTime(self, record, datefmt=None) -> str:
        return f'\x1b[2m{super().formatTime(record, datefmt)}\x1b[0m' # faint
    
    def formatException(self, ei) -> str:
        return f'\x1b[36m{super().formatException(ei)}\x1b[0m' # cyan
    
    def formatStack(self, stack_info) -> str:
        return f'\x1b[36m{super().formatStack(stack_info)}\x1b[0m' # cyan


#---------------------------------------------------------------------------
#   Html Formatter classe
#---------------------------------------------------------------------------

class _HtmlStyleFormatter(logging.Formatter):
    """This is a formatter which add html balises to the record."""
    level_to_color = {
        logging.DEBUG       :   'l1',
        logging.INFO        :   'l2',
        logging.WARNING     :   'l3',
        logging.ERROR       :   'l4',
        logging.CRITICAL    :   'l5'    
    }
 
    def format(self, record) -> str:
        # Do not edit the original record, this let multiple formatters handling the same record
        cpyRecord = copy.copy(record)

        levelcolor = self.level_to_color[cpyRecord.levelno]
        
        cpyRecord.levelname     = f'<span class="{levelcolor}">{cpyRecord.levelname:^9}</span>'
        cpyRecord.name          = f'<span class="{levelcolor}">{cpyRecord.name}</span>'
        cpyRecord.threadName    = f'<span class="{levelcolor}">{cpyRecord.threadName}</span>'
        cpyRecord.msg           = f'<span class="msg">{html.escape(cpyRecord.msg)}</span>'
        return super().format(cpyRecord)

    def formatTime(self, record, datefmt=None) -> str:
        return f'<span class="t">{super().formatTime(record, datefmt)}</span>'
    
    def formatException(self, exc_info) -> str:
        return f'<span class="ei">{html.escape(super().formatException(exc_info))}</span>' 
    
    def formatStack(self, stack_info) -> str:
        return f'<span class="si">{html.escape(super().formatStack(stack_info))}</span>'
    

#---------------------------------------------------------------------------
#   Filter class
#---------------------------------------------------------------------------

class _LogsPackageFilter(logging.Filter):

    def filter(record):
        return record.name.startswith(__package__)
    

#---------------------------------------------------------------------------
#   Logging initialization
#---------------------------------------------------------------------------

_html_metadata = textwrap.dedent('\
    <!DOCTYPE html>\n\
    <head>\n\
      <title>%(name)s logs</title>\n\
      <style>\n\
      body   {color: white; background-color: black; white-space: pre; font-family: monospace; font-size: large}\n\
      .l1    {color: dodgerblue}\n\
      .l2    {color: lawngreen}\n\
      .l3    {color: yellow}\n\
      .l4    {color: crimson}\n\
      .l5    {color: magenta}\n\
      .msg   {color: grey}\n\
      .ei    {color: steelblue}\n\
      .si    {color: steelblue}\n\
      .t     {color: grey}\n\
      </style>\n\
    </head>\n\n\
    ') % bl_info

_html_header = textwrap.dedent('\
    <header>\n\
      Blender version: %(bl_version)s\n\
      Addon version: %(addon_version)s\n\n\
      Blender executable: "%(blender_bin)s"\n\
      Addon directory: "%(addon_path)s"\n\n\
      Platform informations:\n\
        %(platform)s\n\
        %(architecture)s\n\
        %(processor)s\n\
        Python: %(py_version)s\n\
    </header>\n\n\
    ') % _debug_info

with open(file=html_logs_filepath, mode='w', encoding='utf-8') as f:
    f.write(_html_metadata)
    f.write(_html_header)

# Format strings
_min_fmt     = '%(levelname)s %(name)s: %(message)s'
_debug_fmt   = '%(asctime)s %(levelname)s %(name)s from %(threadName)s: %(message)s'

# Define level and format string
_level = logging.WARNING
_fmt = _min_fmt

if LOG_DEBUG:
    _level = logging.DEBUG
    _fmt = _debug_fmt

# Configure Handlers
_console_handler = logging.StreamHandler()
_console_handler.setLevel(_level)
_console_handler.setFormatter(_ConsoleStyleFormatter(_fmt))
_console_handler.addFilter(_LogsPackageFilter)

_html_handler = logging.FileHandler(filename=html_logs_filepath, mode='a', encoding='utf-8')
_html_handler.setLevel(_level)
_html_handler.setFormatter(_HtmlStyleFormatter(fmt=_fmt))
_html_handler.addFilter(_LogsPackageFilter)

# Set root logger level
_root_logger = logging.getLogger()
_root_logger.setLevel(_level)


#---------------------------------------------------------------------------
#   Logs functions
#---------------------------------------------------------------------------

# getLogger re-definition
def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger with the specified name, creating it if necessary.
    
    If no name is specified, return the root logger."""
    return logging.getLogger(name)


# Add handlers to root logger
def start_logging() -> None:
    """Add console & file handlers to the root logger."""
    if _console_handler not in _root_logger.handlers:   
        _root_logger.addHandler(_console_handler)

    if _html_handler not in _root_logger.handlers:
        _root_logger.addHandler(_html_handler)
    
    if LOG_DEBUG:
        get_logger(__name__).warning("DEBUG & INFO logging is enabled !")

   
# Remove handlers from root logger
def stop_logging() -> None:
    """Remove console & file handlers from the root logger."""
    if _console_handler in _root_logger.handlers:   
        _root_logger.removeHandler(_console_handler)
        
    if _html_handler in _root_logger.handlers:
        _root_logger.removeHandler(_html_handler)