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
    """
    logger.debug("HW DRIVER")
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
    for x in led_obj:
        LED(led_obj[x]).off()
    # Accendi il solo GPIO associato al flag
    LED(led_obj[flag]).on()
    return None, None
