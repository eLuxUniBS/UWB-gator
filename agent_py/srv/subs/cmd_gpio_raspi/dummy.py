import logging
import json
from enum import Enum
from gpiozero import LED
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AllarmLedValue(Enum):
    """
    label allarme  =  numero GPIO
    """
    black = 1
    red = 2
    yellow = 3
    green = 4
    white = 5


led_obj = [x.split(".")[-1].strip() for x in list(map(str, AllarmLedValue))]
led_obj = {label.lower().strip(): AllarmLedValue[label] for label in led_obj}


def set_gpio(*args, input_message: dict = None, **kwargs):
    """
    Finge di pilotare dei GPIO
    """
    logger.debug("DUMMY DRIVER")
    print("Input Message in DUMMY Driver",input_message)
    flag = input_message.get("flag", None)
    if flag is None:
        logger.debug("Messaggio vuoto o errato\n{}".format(
            json.dumps(input_message)))
        return None, None
    if flag not in list(led_obj.keys()):
        logger.debug("Messaggio con flag differente\n{}".format(
            json.dumps(input_message)))
        return None, None
    # Spegni tutti i GPIO
    logger.debug("Spengo tutti i led")
    # Accendi il solo GPIO associato al flag
    logger.debug("Accendo il led {}".format(flag))
    return None, None
