import logging
import json
from enum import Enum
#from gpiozero import LED
import RPi.GPIO as GPIO
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AllarmLedValue(Enum):
    """
    label allarme  =  numero GPIO
    """
    black = (0,1,2)
    red = (2,)
    yellow = (1,)
    green = (0,)
    white = ()


led_obj = [x.split(".")[-1].strip() for x in list(map(str, AllarmLedValue))]
led_obj = {label.lower().strip(): AllarmLedValue[label] for label in led_obj}
list_led={"0":dict(val=18,label="LED1",status=False),"1":dict(val=23,label="LED2",status=False),"2":dict(val=24,label="LED3",status=False)}
def init_gpio():
    global list_led
    GPIO.setmode(GPIO.BCM)
    for x in list_led:    
        GPIO.setup(list_led[x].get("val"), GPIO.OUT)

def set_gpio(*args, input_message: dict = None, **kwargs):
    """
    Riceve in input_message la combinazione da inviare ai gpio
    """
    logger.debug("HW DRIVER")
    print("Input Message in HW Driver",input_message)
    flag = input_message.get("flag", None)
    if flag is None:
        logger.debug("Messaggio vuoto o errato\n{}".format(
            json.dumps(input_message)))
        return None, None
    if flag not in list(led_obj.keys()):
        logger.debug("Messaggio con flag differente\n{}".format(
            json.dumps(input_message)))
        return None, None
    if input_message.get("flag",None)is None:
        return None,None
    combo=AllarmLedValue[input_message.get("flag")]
    print("COMBO",combo)
    print("VALUE",combo.value)
    # Turn all off
    for x in list_led:
        list_led[x]["status"]=False
    # Turn only combo value on
    for x in combo.value:
        list_led[str(x)]["status"]=True
    # Set PhyEntity from VirtualEntity
    for x in list_led:
        GPIO.output(list_led[x]["val"],list_led[x]["status"])
    return None, None
