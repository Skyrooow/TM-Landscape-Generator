"""
Implementation of the built-in logging module for the addon.

### Functions:
- Log.Start()       ->  Start handling log messages
- Log.Stop()        ->  Stop handling log messages
- get_logger(name)  ->  Return a logger with the specified name

### Examples
For each file, declare a logger object:
- log = Log.get_logger(__name__)

Logging level | Example
:---|:---
DEBUG     | log.debug("Debug msg", stack_info=True)
INFO      | log.info("Info msg")
WARNING   | log.warning("Warning msg")
ERROR     | log.error("Error msg", stack_info=True)
EXCEPTION | log.exception("Exception msg", stack_info=True)
CRITICAL  | log.critical("Critical msg", stack_info=True)
"""

import logging
import textwrap

from . import Path


LOG_DEBUG = True


# root logger
root_logger = logging.getLogger()


# formatters
console_formatter = logging.Formatter(
    fmt='[%(levelname)s] %(message)s')

debug_console_formatter = logging.Formatter(
    fmt=textwrap.dedent('\
                        [%(levelname)s] (%(name)s) <%(threadName)s>\n\
                          %(message)s'
                        ))

file_formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(message)s')

debug_file_formatter = logging.Formatter(
    fmt=textwrap.dedent('\
                        %(asctime)s [%(levelname)s] (%(name)s) <%(threadName)s>\n\
                          %(message)s'
                        ))


# handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=Path.get_logfile_path(), mode='w', encoding='utf-8')


# Set level and formatters
if LOG_DEBUG:
    root_logger.setLevel(logging.DEBUG)

    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(debug_console_formatter)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(debug_file_formatter)
else:
    root_logger.setLevel(logging.WARNING)

    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_formatter)

    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(file_formatter)


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