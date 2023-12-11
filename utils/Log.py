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

import logging, copy, textwrap

from . import Path




LOG_DEBUG = True


#---------------------------------------------------------------------------
#   Initialise html log file
#---------------------------------------------------------------------------

logfile = Path.get_logfile_path()

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

with open(file=logfile, mode='w', encoding='utf-8') as f:
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
        # Do not edit the original record, this let multiple formatter handling the same record 
        cpyRecord = copy.copy(record) 

        levelcolor = self.level_to_color[cpyRecord.levelno]

        cpyRecord.levelname    = '\x1b[1;3%sm%s\x1b[0m'     % (levelcolor, '{:^8s}'.format(cpyRecord.levelname))
        cpyRecord.name         = '\x1b[1;3%sm%s\x1b[0m'     % (levelcolor, cpyRecord.name)
        cpyRecord.threadName   = '\x1b[1;3%sm%s\x1b[0m'     % (levelcolor, cpyRecord.threadName)
        cpyRecord.message      = '\x1b[2m%s\x1b[0m'         % (cpyRecord.getMessage())
        if self.usesTime():
            cpyRecord.asctime  = '\x1b[2m%s\x1b[0m'         % (self.formatTime(cpyRecord, self.datefmt))
        s = self.formatMessage(cpyRecord)
        if cpyRecord.exc_info:
            if not cpyRecord.exc_text:
                cpyRecord.exc_text = self.formatException(cpyRecord.exc_info)
        if cpyRecord.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + cpyRecord.exc_text
        if cpyRecord.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(cpyRecord.stack_info)
        return s


    def formatException(self, ei) -> str:
        return '\x1b[36m%s\x1b[0m' % (super().formatException(ei))
    
    
    def formatStack(self, stack_info) -> str:
        return '\x1b[36m%s\x1b[0m' % (super().formatStack(stack_info))


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
        # Do not edit the original record, this let multiple formatter handling the same record
        cpyRecord = copy.copy(record)

        levelcolor = self.level_to_color[cpyRecord.levelno]

        cpyRecord.levelname    = '<span class="%s">%s</span>'     % (levelcolor, '{:^8s}'.format(cpyRecord.levelname))
        cpyRecord.name         = '<span class="%s">%s</span>'     % (levelcolor, cpyRecord.name)
        cpyRecord.threadName   = '<span class="%s">%s</span>'     % (levelcolor, cpyRecord.threadName)
        cpyRecord.message      = '<span class="msg">%s</span>'  % (cpyRecord.getMessage()).replace('&', '&#38').replace('<','&#60')
        if self.usesTime():
            cpyRecord.asctime  = '<span class="t">%s</span>'   % (self.formatTime(cpyRecord, self.datefmt))
        s = self.formatMessage(cpyRecord)
        if cpyRecord.exc_info:
            if not cpyRecord.exc_text:
                cpyRecord.exc_text = self.formatException(cpyRecord.exc_info)
        if cpyRecord.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + cpyRecord.exc_text
        if cpyRecord.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(cpyRecord.stack_info)
        return '%s' % (s)

    def formatException(self, exc_info) -> str:
        return '<span class="ei">%s</span>' % super().formatException(exc_info).replace('&', '&#38').replace('<','&#60')
    
    def formatStack(self, stack_info) -> str:
        return '<span class="si">%s</span>' % super().formatStack(stack_info).replace('&', '&#38').replace('<','&#60')
    

#---------------------------------------------------------------------------
#   Log configuration
#---------------------------------------------------------------------------

root_logger = logging.getLogger()

# Format strings
min_fmt     = '%(levelname)s %(name)s: %(message)s'
debug_fmt   = '%(asctime)s %(levelname)s %(name)s from %(threadName)s: %(message)s'

# Console formatters
console_formatter = ConsoleStyleFormatter(fmt=min_fmt)
debug_console_formatter = ConsoleStyleFormatter(fmt=debug_fmt)

# Html formatters
html_formatter = HtmlStyleFormatter(fmt=min_fmt)
debug_html_formatter = HtmlStyleFormatter(fmt=debug_fmt)

#Handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=logfile, mode='a', encoding='utf-8')

# Set level and formatters
if LOG_DEBUG:
    root_logger.setLevel(logging.DEBUG)

    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(debug_console_formatter)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(debug_html_formatter)
else:
    root_logger.setLevel(logging.WARNING)

    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_formatter)

    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(html_formatter)


#---------------------------------------------------------------------------
#   Log functions
#---------------------------------------------------------------------------

# Add handlers to root logger
def start() -> None:
    """Add console & file handlers to the root logger."""
    if console_handler not in root_logger.handlers:   
        root_logger.addHandler(console_handler)

    if file_handler not in root_logger.handlers:
        root_logger.addHandler(file_handler)
    
    if LOG_DEBUG:
        root_logger.warning("DEBUG & INFO logging is enabled !")
   

# Remove handlers from root logger
def stop() -> None:
    """Remove console & file handlers from the root logger."""
    if console_handler in root_logger.handlers:   
        root_logger.removeHandler(console_handler)
        #console_handler.close()

    if file_handler in root_logger.handlers:
        root_logger.removeHandler(file_handler)
        #file_handler.close()


# getLogger re-definition
def getLogger(name: str | None = None) -> logging.Logger:
    """Return a logger with the specified name, creating it if necessary.

If no name is specified, return the root logger."""
    return logging.getLogger(name)