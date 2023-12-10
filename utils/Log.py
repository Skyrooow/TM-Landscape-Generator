import logging
import textwrap

from . import Path

from .. import LOG_DEBUG




# root logger
root_logger = logging.getLogger()


# log level
root_level: int
if LOG_DEBUG:
    root_level = logging.DEBUG
else:
    root_level = logging.WARNING


# handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=Path.get_logfile_path(), mode='w', encoding='utf-8')


# formatters
min_formatter = logging.Formatter(
    fmt=textwrap.dedent('\
                        %(levelname)s: %(name)s\n\
                        .. "%(message)s"'),
    datefmt='%Y-%m-%d %H:%M:%S',
    style='%')

full_formatter = logging.Formatter(
    fmt=textwrap.dedent('\
                        %(levelname)s: %(name)s\n\
                        .. file "%(pathname)s", Line %(lineno)s, in %(funcName)s\n\
                        .. "%(message)s"'),
    datefmt='%Y-%m-%d %H:%M:%S',
    style='%')
    

# set log level
root_logger.setLevel(root_level)
console_handler.setLevel(root_level)
file_handler.setLevel(root_level)


# set formatter
console_handler.setFormatter(min_formatter)
file_handler.setFormatter(full_formatter)



# get logger re-definition
def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger with the specified name, creating it if necessary.

If no name is specified, return the root logger."""
    return logging.getLogger(name)


# add handlers to root logger
def start() -> None:
    """Add console & file handlers to the root logger."""
    if console_handler not in root_logger.handlers:   
        root_logger.addHandler(console_handler)

    if file_handler not in root_logger.handlers:
        root_logger.addHandler(file_handler)

    if LOG_DEBUG:
        root_logger.warning("DEBUG & INFO logging is enabled !")


# free handlers
def stop() -> None:
    """Remove console & file handlers from the root logger."""
    if console_handler in root_logger.handlers:   
        root_logger.removeHandler(console_handler)

    if file_handler in root_logger.handlers:
        root_logger.removeHandler(file_handler)