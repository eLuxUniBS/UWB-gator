import logging
from enum import Enum
from typing import Callable
from datetime import datetime as dt

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ColorCode(Enum):
    """
    Associazione codici in centimetri
    """
    black = (-100, 500)
    red = (500, 1000)
    yellow = (1000, 1500)
    green = (1500, 3000)
    white = (3000, 5000)


def unitn_raw_parse_message(*args, id_send: str = None, input_message: str = None, ts_collected: dt = None, **kwargs) -> dict:
    """
    Funzione parsing riga seriale Firmware UniTN v2. Se riesce, allora ho una struttura, altrimenti ho una sua versione incompleta;
    la struttura ritornata contiene in raw_content il messaggio originale
    """
    id_send = id_send if id_send is not None else ""
    if input_message is None:
        logger.debug("Messaggio vuoto, pertanto inutile proseguire")
        return None, dict(
            header=dict(
                id_send=id_send,
                ts_send=dt.utcnow().timestamp()
            ),
            payload=None)
    # Parsing messaggio con successo!
    scheme = dict(raw_distance=dict(val=None, label="SUCCESS"), distance=dict(val=None, label="bias"),
                  first_peak_pwr=dict(val=None, label="fppwr"), receive_power=dict(val=None, label="rxpwr"),
                  frequency_offset=dict(val=None, label="cifo"))
    struct_message = dict(detected=True)
    # DOC Formato messaggio corretto
    # SUCCESS raw_distance bias distance fppwr first_peak_pwr rxpwr receive_power cifo frequency_offset
    try:
        # Add ts collected
        struct_message["ts_collected"] = ts_collected if ts_collected is not None else dt.utcnow()
        struct_message["ts_collected"] = struct_message["ts_collected"].__str__()
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
        # Retrieve sender-receiver, eg. c517->8615
        try:
            index_base = list_message.index("SUCCESS") - 1
            if index_base >= 0:
                struct_message["sender"], struct_message["receiver"] = [x.replace(
                    ":", "") for x in list_message[index_base].split("->") if len(x.strip()) > 0]
        except Exception as e:
            struct_message["sender"] = None
            struct_message["receiver"] = None
        return None, dict(
            header=dict(
                id_send=id_send,
                ts_send=dt.utcnow().timestamp()
            ),
            payload=struct_message)
    except Exception as e:
        print(e)
    struct_message["detected"] = False
    struct_message["raw_content"] = input_message
    return None, dict(
        header=dict(
            id_send=id_send,
            ts_send=dt.utcnow().timestamp()
        ),
        payload=struct_message)


def unitn_raw_detect_allarm(*args, consider_raw_distance: bool = False, consider_distance: bool = True, **kwargs):
    """
    Recupera dalla seriale l'informazione corretta ed in base alla distanza misurata, indica quale allarme deve essere attivato
    """
    _, message_content = unitn_raw_parse_message(
        id_send=kwargs.get("id_send", None),
        input_message=kwargs.get("input_message", None),
        ts_collected=kwargs.get("ts_collected", None)
    )
    if message_content is None:
        return None, None
    if not message_content.get("payload", dict()).get("detected", False):
        return None, None
    message = dict(allert_distance="", id="{send}->{res}".format(
        send=message_content.get("payload", dict()).get("sender", ""),
        res=message_content.get("payload", dict()).get("receiver", "")
    ), flag="", distance="",raw_distance="")
    if consider_distance == consider_raw_distance == False:
        return None, None
    elif consider_distance:
        message["allert_distance"] = message_content.get(
            "payload", dict()).get("distance", "")
    
    elif consider_raw_distance:
        message["allert_distance"] = message_content.get(
            "payload", dict()).get("raw_distance", "")
    message["raw_distance"] = message_content.get(
        "payload", dict()).get("raw_distance", "")
    message["distance"] = message_content.get(
        "payload", dict()).get("distance", "")
    # Passaggio dai valori numerici ad un flag testuale    
    buffer = [x.split(".")[-1] for x in list(map(str, ColorCode))]    
    for field, scale in [(x, ColorCode[x]) for x in buffer]:
        if float(min(scale.value)) < float(message["allert_distance"]) <= float(max(scale.value)):
            message["flag"] = str(field).strip().lower()
    print("\n[MESSAGE][",dt.utcnow(),"]",message)
    return None, message
