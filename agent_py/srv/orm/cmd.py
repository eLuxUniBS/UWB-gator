import logging
from srv.orm import influxdb, mongo
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


def save_net(*args, db_ref: str = "serial", input_message: dict = None, log_data: bool = True, **kwargs):
    if db_ref == "serial":
        influxdb.client.last.query(content=input_message)
        if log_data:
            influxdb.client.log.query(content=input_message)
        return None, None
    elif db_ref == "rel":
        pass
    elif db_ref == "unrel":
        pass
    else:
        return None, None


def read_net(*args, db_ref: str = "serial", input_message: dict = None, ** kwargs):
    """
    Funzione specifica per leggere una qualsiasi rete
    """
    if db_ref == "serial":
        content = influxdb.client.last.query(content=dict(query="get"))
        dataset=[]
        print("CONTENT")
        print(content)
        # for single_content in content:
        #     pass
        return None, content
    elif db_ref == "rel":
        pass
    elif db_ref == "unrel":
        pass
    else:
        return None, None
