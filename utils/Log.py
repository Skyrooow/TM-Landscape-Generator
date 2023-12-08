import logging

from . import Path


# Configure the main logger
def get_master_logger(name: str | None = None, debug: bool = False) -> logging.Logger:
    """Return the master logger, must be called only once in main __init__.py with name = __name__"""
    logger = logging.getLogger(name)    
    logger.setLevel(logging.DEBUG)

    # formaters
    full_formatter = logging.Formatter(
    fmt='%(levelname)s: %(name)s\n\
        file "%(pathname)s", Line %(lineno)s, in %(funcName)s\n\
        "%(message)s"\n',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='%')

    min_formatter = logging.Formatter(
    fmt='%(levelname)s: %(name)s\n\
        "%(message)s"',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='%')

    # handlers
    file_handler = logging.FileHandler(filename=Path.get_logfile_path(), mode='w', encoding='utf-8')
    console_handler = logging.StreamHandler()
    
    if debug:
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(full_formatter)
        
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(min_formatter)
    else:
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(full_formatter)

        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(min_formatter)
        
    # add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger, name should be __name__ to follow module-level hierarchy"""
    return logging.getLogger(name)
    

