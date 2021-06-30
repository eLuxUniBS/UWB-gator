import logging
from typing import Callable
from datetime import datetime as dt

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def parsing_message_unitn(*args, input_message: str = None, ts_collected: dt = None, **kwargs) -> dict:
    """
    Funzione parsing riga seriale Firmware UniTN v2. Se riesce, allora ho una struttura, altrimenti ho una sua versione incompleta;
    la struttura ritornata contiene in raw_content il messaggio originale
    """
    if input_message is None:
        logger.debug("Messaggio vuoto, pertanto inutile proseguire")
        return None,None
    # Parsing messaggio con successo!
    scheme = dict(raw_distance=dict(val=None, label="SUCCESS"), distance=dict(val=None, label="bias"),
                  first_peak_pwr=dict(val=None, label="fppwr"), receive_power=dict(val=None, label="rxpwr"),
                  frequency_offset=dict(val=None, label="cifo"))
    struct_message = dict(detected=True)
    # SUCCESS raw_distance bias distance fppwr first_peak_pwr rxpwr receive_power cifo frequency_offset
    try:
        # Add ts collected
        struct_message["ts_collected"] = ts_collected if ts_collected is not None else dt.utcnow()
        struct_message["ts_collected"]=struct_message["ts_collected"].__str__()
        # Try to filter data
        list_message = [x.strip() for x in input_message.strip().split(" ")]
        for single_item in scheme.keys():
            if list_message.count(scheme[single_item]["label"]) == 0:
                struct_message["detected"] = False
            else:
                index_base = list_message.index(scheme[single_item]["label"])
                if (index_base + 1) < len(list_message):
                    struct_message[single_item] = list_message[index_base + 1]
        # Add Raw
        struct_message["raw_content"] = input_message
        # Retriece sender-receiver, eg. c517->8615
        try:
            index_base = list_message.index("SUCCESS") - 1
            if index_base >= 0:
                struct_message["sender"], struct_message["receiver"] = [x.replace(
                    ":", "") for x in list_message[index_base].split("->") if len(x.strip()) > 0]
        except Exception as e:
            struct_message["sender"] = None
            struct_message["receiver"] = None
        return None,struct_message
    except Exception as e:
        print(e)
    struct_message["detected"] = False
    struct_message["raw_content"] = input_message
    return None,struct_message
