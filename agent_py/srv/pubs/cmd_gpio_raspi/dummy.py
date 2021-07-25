import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def set_gpio(*args,**kwargs):
    logger.debug("DUMMY DRIVER")