import time
import logging
import json
import mqttools
from serial import Serial

logger = logging.getLogger(__name__)
BROKER_PORT = 30000


def parsing_serial(*args, raw_message: str = None, ts_collected: time.time = None, **kwargs) -> dict:
    logger.debug("{}INIT\n{}\nEND".format(time.time(), raw_message))
    if raw_message is None:
        logger.debug("Messaggio vuoto, pertanto inutile proseguire")
        return None
    # Parsing messaggio con successo!
    scheme = dict(raw_distance=dict(val=None, label="SUCCESS"), distance=dict(val=None, label="bias"),
                  first_peak_pwr=dict(val=None, label="fppwr"), receive_power=dict(val=None, label="rxpwr"),
                  frequency_offset=dict(val=None, label="cifo"))
    struct_message = dict(detected=True)
    # SUCCESS raw_distance bias distance fppwr first_peak_pwr rxpwr receive_power cifo frequency_offset
    try:
        # Add ts collected
        struct_message["ts_collected"] = ts_collected if ts_collected is not None else dt.utcnow()
        # Try to filter data
        list_message = [x.strip() for x in raw_message.strip().split(" ")]
        for single_item in scheme.keys():
            if list_message.count(scheme[single_item]["label"]) == 0:
                struct_message["detected"] = False
            else:
                index_base = list_message.index(scheme[single_item]["label"])
                if (index_base + 1) < len(list_message):
                    struct_message[single_item] = list_message[index_base + 1]
        # Add Raw
        struct_message["raw_content"] = raw_message
        # Retriece sender-receiver c517->8615
        try:
            index_base = list_message.index("SUCCESS") - 1
            if index_base >= 0:
                struct_message["sender"], struct_message["receiver"] = [x.replace(
                    ":", "") for x in list_message[index_base].split("->") if len(x.strip()) > 0]
        except Exception as e:
            struct_message["sender"] = None
            struct_message["receiver"] = None
        return struct_message
    except Exception as e:
        print(e)
    struct_message["detected"] = False
    struct_message["raw_content"] = raw_message
    return struct_message


async def pubMeasurementFromSerial(subs: str = "net/geo",
                                    server="localhost",
                                    port=BROKER_PORT,
                                    topic="/p2p/data",
                                    serial_path: str = None,
                                    id_send:str=None,
                                    baudrate: int = 115200,
                                    timeout: int = 1):
    if id_send is None:
        id_send=serial_path.split("/")[-1]
    print("ID",id_send,"PATH",serial_path)
    while True:        
        cli = Serial(serial_path, baudrate=baudrate, timeout=timeout)
        async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
            while True:
                try:
                    buffer = cli.readline(1024)
                    # print(buffer.decode("utf-8"))
                    response = parsing_serial(raw_message=buffer.decode(
                        "utf-8"), ts_collected=time.time())
                    # response = client.publish(
                    #     topic, json.dumps(message).encode('utf-8'))
                    if response.get("detected", False):
                        buffer = dict(header=dict(
                            ts_send=time.time(),
                            id_send=id_send
                            ), payload=response)
                        mqtt_resp = client.publish(
                            topic, json.dumps(buffer).encode('utf-8'))
                        print(time.time(), "\t", buffer["payload"]["raw_distance"], "~", buffer["payload"]["distance"], "\nwrite to {} --- this message".format(topic),
                              "\nMessage", buffer, "\nResponse", mqtt_resp)
                        # time.sleep(2)
                except Exception as e:
                    print("ERRORE", e)
                    break
