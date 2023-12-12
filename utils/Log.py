"""
Formatted logging with colors in console & in html file

### Functions:
- Log.Start()       ->  Start handling log messages
- Log.Stop()        ->  Stop handling log messages
- getLogger(name)  ->  Return a logger with the specified name

### Examples
For each file, declare a logger object:
- log = Log.getLogger(__name__)

Logging level | Example | Note
:---|:---|:---
DEBUG     | log.debug("Debug msg", stack_info=True)
INFO      | log.info("Info msg")
WARNING   | log.warning("Warning msg")
EXCEPTION | log.exception("Exception msg") | Inside of Except block only              
ERROR     | log.error("Error msg", stack_info=True)
CRITICAL  | log.critical("Critical msg", stack_info=True)
"""

import logging, copy, textwrap, html

from . import Path




LOG_DEBUG = True


#---------------------------------------------------------------------------
#   Initialise html log file
#---------------------------------------------------------------------------

htmlfile = Path.get_logfile_path()

htmlHeader = textwrap.dedent('\
                             <!DOCTYPE html>\n\
                             <style>\n\
                             body   {color: white; background-color: black; white-space: pre; font-family: monospace; font-size: large;}\n\
                             .l1    {color: dodgerblue}\n\
                             .l2    {color: lawngreen}\n\
                             .l3    {color: yellow}\n\
                             .l4    {color: crimson}\n\
                             .l5    {color: magenta}\n\
                             .msg   {color: grey}\n\
                             .ei    {color: steelblue;}\n\
                             .si    {color: steelblue;}\n\
                             .t     {color: grey;}\n\
                             </style>\n\n\
                            ')

with open(file=htmlfile, mode='w', encoding='utf-8') as f:
    f.write(htmlHeader)

#---------------------------------------------------------------------------
#   Console Formatter classe
#---------------------------------------------------------------------------

class ConsoleStyleFormatter(logging.Formatter):
    """
    This is a formatter which add escape codes to the record.
    
    https://gist.github.com/abritinthebay/d80eb99b2726c83feb0d97eab95206c4
    """
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    level_to_color = {
        logging.DEBUG       :   BLUE,
        logging.INFO        :   GREEN,
        logging.WARNING     :   YELLOW,
        logging.ERROR       :   RED,
        logging.CRITICAL    :   MAGENTA   
    }

    def format(self, record) -> str:
        # Do not edit the original record, this let multiple formatters handling the same record 
        cpyRecord = copy.copy(record) 

        levelcolor = self.level_to_color[cpyRecord.levelno]

        cpyRecord.levelname     = '\x1b[1;3%sm%s\x1b[0m'    % (levelcolor, '{:^9s}'.format(cpyRecord.levelname))
        cpyRecord.name          = '\x1b[1;3%sm%s\x1b[0m'    % (levelcolor, cpyRecord.name)
        cpyRecord.threadName    = '\x1b[1;3%sm%s\x1b[0m'    % (levelcolor, cpyRecord.threadName)
        cpyRecord.msg           = '\x1b[2m%s\x1b[0m'        % (cpyRecord.getMessage())
        return super().format(cpyRecord)

    def formatTime(self, record, datefmt=None) -> str:
        return '\x1b[2m%s\x1b[0m' % super().formatTime(record, datefmt)
    
    def formatException(self, ei) -> str:
        return '\x1b[36m%s\x1b[0m' % super().formatException(ei)
    
    def formatStack(self, stack_info) -> str:
        return '\x1b[36m%s\x1b[0m' % super().formatStack(stack_info)


#---------------------------------------------------------------------------
#   Html Formatter classe
#---------------------------------------------------------------------------

class HtmlStyleFormatter(logging.Formatter):
    """
    This is a formatter which add html balises to the record.  
    """
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
        
        cpyRecord.levelname     = '<span class="%s">%s</span>'  % (levelcolor, '{:^9s}'.format(cpyRecord.levelname))
        cpyRecord.name          = '<span class="%s">%s</span>'  % (levelcolor, cpyRecord.name)
        cpyRecord.threadName    = '<span class="%s">%s</span>'  % (levelcolor, cpyRecord.threadName)
        cpyRecord.msg           = '<span class="msg">%s</span>' % html.escape(cpyRecord.getMessage())
        return super().format(cpyRecord)

    def formatTime(self, record, datefmt=None) -> str:
        return '<span class="t">%s</span>' % super().formatTime(record, datefmt)
    
    def formatException(self, exc_info) -> str:
        return '<span class="ei">%s</span>' % html.escape(super().formatException(exc_info))
    
    def formatStack(self, stack_info) -> str:
        return '<span class="si">%s</span>' % html.escape(super().formatStack(stack_info))
    

#---------------------------------------------------------------------------
#   Log configuration
#---------------------------------------------------------------------------

root_logger = logging.getLogger()

# Format strings
min_fmt     = '%(levelname)s %(name)s: %(message)s'
debug_fmt   = '%(asctime)s %(levelname)s %(name)s from %(threadName)s: %(message)s'

#Handlers
console_handler = logging.StreamHandler()
html_handler = logging.FileHandler(filename=htmlfile, mode='a', encoding='utf-8')

# Set level and formatters
level = logging.WARNING
fmt = min_fmt

if LOG_DEBUG:
    level = logging.DEBUG
    fmt = debug_fmt

root_logger.setLevel(level)
console_handler.setLevel(level)
html_handler.setLevel(level)

console_handler.setFormatter(ConsoleStyleFormatter(fmt=fmt))
html_handler.setFormatter(HtmlStyleFormatter(fmt=fmt))


#---------------------------------------------------------------------------
#   Log functions
#---------------------------------------------------------------------------

# getLogger re-definition
def getLogger(name: str | None = None) -> logging.Logger:
    """Return a logger with the specified name, creating it if necessary.

If no name is specified, return the root logger."""
    return logging.getLogger(name)


# Add handlers to root logger
def start() -> None:
    """Add console & file handlers to the root logger."""
    if console_handler not in root_logger.handlers:   
        root_logger.addHandler(console_handler)

    if html_handler not in root_logger.handlers:
        root_logger.addHandler(html_handler)
    
    if LOG_DEBUG:
        getLogger(__name__).warning("DEBUG & INFO logging is enabled !")

   
# Remove handlers from root logger
def stop() -> None:
    """Remove console & file handlers from the root logger."""
    if console_handler in root_logger.handlers:   
        root_logger.removeHandler(console_handler)
        
    if html_handler in root_logger.handlers:
        root_logger.removeHandler(html_handler)