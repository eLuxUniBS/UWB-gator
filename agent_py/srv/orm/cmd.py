import logging
import json
from agent_py.srv.orm import influxdb, mongo
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def query_serial(*args, **kwargs):
    """
    """
    # TODO WIP
    print("query_serial")
    print("ARGS", args)
    print("KWARGS", kwargs)
    return None, None


def query_unrel(*args, **kwargs):
    """
    """
    # TODO WIP
    print("query_unrel")
    print("ARGS", args)
    print("KWARGS", kwargs)
    return None, None


def save_serial_data(*args, input_message: dict = None, mark_ts, **kwargs):
    """
    Utility specifica per salvare i dati: se nel payload del messaggio input, esiste un campo detected con valore True, viene salvato in aggiunta in una collection di GoodSignal
    """
    if input_message.get("payload", dict()).get("detected", False):
        logger.debug("GoodSignal")
        mongo.GoodSignal.create(header=input_message.get(
            "header"), body=input_message.get("payload"))
    logger.debug("RawSignal")
    mongo.RawSignal.create(header=input_message.get(
        "header"), body=input_message.get("payload"))
    return None, None


def save_net(*args, db_ref: str = "serial", input_message: dict = None, log_data: bool = True, filter_mac_permitted: list = None, **kwargs):
    if db_ref == "serial":
        influxdb.client.last.query(content=input_message)
        if log_data:
            influxdb.client.log.query(content=input_message)
        return None, None
    elif db_ref == "rel":
        pass
    elif db_ref == "unrel":
        if input_message.get("payload", dict()).get("query", "") != "save":
            return None, None
        """
        Singolo
        {'header': 'Sonda 1_705c2e14-cb37-4c22-b04e-ab30e412e31c', 
        'payload': {
            'query': 'save', 
            'params': {'index': '0', 'qos': 'MqttQos.atMostOnce'}, 
            'data': {'fields': {'mac': 'D5:4E:F4:0C:F6:26', 'x': 9708547.0, 'y': 1677721600.0, 'z': 25581096.0, 'q': 0.0}, 'tags': {'id': 'DW0AB5', 'ts': '1626944411844716'}}}}
        """
        """
           Multi
           {
               'header': 'null_17774433-d4e0-4a0e-bcc5-32e31da66a51',
               'payload': {
                'query': 'save', 
                'params': {'id': '2021-07-22 09:00:55.227609Z', 'index': '0', 'qos': 'MqttQos.atMostOnce'},
                'data': '{
                        "data_sendit":[],
                        "flags":{"client_id":null,"ts":"2021-07-22 09:00:55.227586Z"},
                        "data":[{
                                "ts":"2021-07-22 09:00:55.180386Z",
                                "params":{"id":"DW0AB5"},
                                "obj":"{\\"header\\":\\"Sonda 1_6c587aa2-3320-440a-b608-0f9bd8bb3503\\",\\"payload\\":{\\"query\\":\\"save\\",\\"params\\":{\\"index\\":\\"0\\",\\"qos\\":\\"MqttQos.atMostOnce\\"},\\"data\\":{\\"fields\\":{\\"mac\\":\\"D5:4E:F4:0C:F6:26\\",\\"x\\":9708547.0,\\"y\\":1677721600.0,\\"z\\":29251112.0,\\"q\\":0.0},\\"tags\\":{\\"id\\":\\"DW0AB5\\",\\"ts\\":\\"1626944455180330\\"}}}}"},{"ts":"2021-07-22 09:00:55.225387Z","params":{"id":"DW0AB5"},"obj":"{\\"header\\":\\"Sonda 1_6c587aa2-3320-440a-b608-0f9bd8bb3503\\",\\"payload\\":{\\"query\\":\\"save\\",\\"params\\":{\\"index\\":\\"0\\",\\"qos\\":\\"MqttQos.atMostOnce\\"},\\"data\\":{\\"fields\\":{\\"mac\\":\\"D5:4E:F4:0C:F6:26\\",\\"x\\":9708547.0,\\"y\\":1677721600.0,\\"z\\":25581096.0,\\"q\\":0.0},\\"tags\\":{\\"id\\":\\"DW0AB5\\",\\"ts\\":\\"1626944455225328\\"}}}}"
                                }]
                        }'
                }
            }
        """
        buffer = input_message.get("payload", dict()).get("data", dict())
        if type(buffer) == str:
            buffer = json.loads(buffer)
            buffer = buffer.get("data")
            buffer = [json.loads(x.get("obj")).get(
                "payload", dict()).get("data", dict()) for x in buffer]
        elif buffer.get("fields", None) is not None:
            buffer = [buffer]
        else:
            return None, None
        buffer = [{**single.get("fields", dict()), **single.get("tags", dict())}
                  for single in buffer]
    else:
        return None, None
    if filter_mac_permitted is not None:
        buffer = [x for x in buffer if x.get(
            "mac", "").strip().lower() in filter_mac_permitted]
    mongo.Last.create(input_data=buffer)
    if log_data:
        mongo.Log.create(input_data=buffer)    
    return None, None


def read_net(*args, db_ref: str = "serial", input_message: dict = None, ** kwargs):
    """
    Funzione specifica per leggere una qualsiasi rete
    """
    if db_ref == "serial":
        content = influxdb.client.last.query(content=dict(query="get"))
        return None, content
    elif db_ref == "rel":
        pass
    elif db_ref == "unrel":
        print("CONTENT")
        print(content)
    else:
        return None, None
