
import logging
import json
import time
import mqttools
from datetime import datetime as dt
from typing import Callable
from serial import Serial
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def ping(*args, input_message: dict = None, time_wait_before: float = 0.0, time_wait_after: float = .0, **kwargs) -> tuple:
    """
    Funzionalità di ping per il test della comunicazione
    """
    time.sleep(time_wait_before)
    ts = dt.utcnow().__str__()
    logger.debug("PING{ts} con messaggio {input_message}\n Altri parametri\n args={args} kwargs={kwargs}".format(
        ts=ts,
        input_message=input_message if input_message is not None else "{}",
        args=",".join(args),
        kwargs=",".join(["{}:{}".format(k, kwargs.get(k, "-missing-").__str__()) for k in kwargs.keys()]))
    )
    time.sleep(time_wait_after)
    return None, {"ping": "pong", "ts": ts}


async def wrapper_callback_sub(*args, cb: Callable = ping, channel: str = None, host: str = None, port: int = None, connection_delays: list = None, turn_off_with_empty_topic: bool = False, topic_response: str = None, time_wait_before: float = 0.0, time_wait_after: float = 0.0, **kwargs):
    """
    Subscriber Wrapper
    - cb è una funzione definita 
    - cb riceve in ingresso nel campo input_message il messaggio ricevuto sul canale
    - cb riceve anche tutti i parametri definiti in *args e **kwargs
    - cb pubbica una tupla dove il primo elemento è il topic per il messaggio successivo, mentre il secondo il messaggio da inviare
    - *args e **kwargs sono passati direttamente in cb
    """
    # Pulizia parametri
    channel = channel if channel is not None else "/test"
    host = host if host is not None else "localhost"
    port = port if port is not None else 1883
    connection_delays = connection_delays if connection_delays is not None and len(
        connection_delays) > 0 and type(connection_delays[0]) == float else [0.1]
    # Avvio servizio
    client = mqttools.Client(host=host, port=port,
                             connect_delays=connection_delays)
    await client.start()
    await client.subscribe(channel)
    while True:
        time.sleep(time_wait_before)
        logger.debug("Attesa ricezione")
        topic, byte_content = await client.messages.get()
        try:
            logger.debug("Ricezione messaggio {}".format(topic))
        except Exception as e:
            logger.warning("Errore lettura topic")
            continue
        if byte_content is None:
            logger.warning("Messaggio vuoto per topic {}".format(topic))
            continue
        try:
            content = json.loads(byte_content.decode('utf-8'))
        except Exception as e:
            logger.warning("Errore decodifica json content utf8")
            logger.debug("Errore\n{}".format(e.__str__()))
            continue
        if topic is None and turn_off_with_empty_topic:
            logger.info("Chiusura topic")
            return
        try:
            logger.debug("Call CB IN SUB {}@{}".format(channel,
                                                       dt.utcnow().__str__()))
            cb_topic, cb_response = cb(*args, input_message=content, **kwargs)
            if cb_topic == None:
                cb_topic = topic_response
            if cb_response == None:
                cb_response = dict()
            if cb_topic is not None:
                logger.debug("Emissione messaggio dal canale {} con topic {}".format(
                    channel, cb_topic))
                cb_response = json.dumps(cb_response).encode("utf-8")
                client.publish(topic=cb_topic, message=cb_response)
        except Exception as e:
            logger.warning("Errore CB SUBS")
            print(e)
            logger.debug("Errore esecuzione callback\n{}".format(e.__str__()))
        time.sleep(time_wait_after)


async def wrapper_callback_pub(
        *args,
        cb: Callable = ping,
        channel: str = None,
        host: str = None,
        port: int = None, connection_delays: list = None, time_wait_before: float = 0.0, time_wait_after: float = 0.0, **kwargs):
    """
    Publisher Wrapper
    - cb è una funzione definita 
    - cb riceve in ingresso tutti i parametri *args e **kwargs
    - cb pubbica una tupla dove il primo elemento è il topic per il messaggio successivo, mentre il secondo il messaggio da inviare
    - *args e **kwargs sono passati direttamente in cb
    """
    # Pulizia parametri
    channel = channel if channel is not None else "/test"
    host = host if host is not None else "localhost"
    port = port if port is not None else 1883
    connection_delays = connection_delays if connection_delays is not None and len(
        connection_delays) > 0 and type(connection_delays[0]) == float else [0.1]
    # Avvio servizio
    async with mqttools.Client(host=host, port=port, connect_delays=connection_delays) as client:
        while True:
            try:
                time.sleep(time_wait_before)
                logger.debug("Call CB IN PUB {}@{}".format(channel,
                                                           dt.utcnow().__str__()))
                cb_topic, cb_response = cb(*args, **kwargs)
                if cb_topic == None:
                    cb_topic = channel
                if cb_response == None:
                    cb_response = dict()
                if cb_topic is not None:
                    logger.debug("Invio messaggio {}".format(cb_topic))
                    cb_response = json.dumps(cb_response).encode("utf-8")
                    client.publish(topic=cb_topic, message=cb_response)
            except Exception as e:
                print(e)
                logger.warning("Errore CB PUB")
                logger.debug(
                    "Errore esecuzione callback\n{}".format(e.__str__()))
            time.sleep(time_wait_after)


async def wrapper_serial_callback_pub(
    *args, serial_path, id_send: str = None,
    baudrate: int = 115200,
    timeout: int = 1, buffer_read: int = 1024,
    cb: Callable = ping, channel: str = None,
    host: str = None, port: int = None,
    connection_delays: list = None,
    time_wait_before: float = 0.0,
    time_wait_after: float = 1.0,
        **kwargs):
    """
    Wrapper per gestire i servizi publisher che trasferiscono i dati provenienti dalla seriale al broker mqtt
    
    """
    # Pulizia parametri
    channel = channel if channel is not None else "/test"
    host = host if host is not None else "localhost"
    port = port if port is not None else 1883
    connection_delays = connection_delays if connection_delays is not None and len(
        connection_delays) > 0 and type(connection_delays[0]) == float else [0.1]
    # Avvio servizio
    logger.debug("Mqtt config:{}@{}:{}".format(channel,host,port))
    logger.debug("Inizio Seriale {}:{}@{}".format(host,port,serial_path))
    while True:
        cli = Serial(serial_path, baudrate=baudrate, timeout=timeout)
        try:
            async with mqttools.Client(host=host, port=port, connect_delays=connection_delays) as client:
                while True:
                    try:
                        time.sleep(time_wait_before)
                        logger.debug("ReadLine")
                        buffer = cli.readline(buffer_read)
                        cb_topic, cb_response = cb(
                            *args,
                            id_send=id_send,
                            input_message=buffer.decode("utf-8"),
                            **kwargs
                        )
                        logger.debug("Verifica")
                        logger.debug("Topic {}".format(cb_topic))
                        if cb_topic == None:
                            cb_topic = channel
                        if cb_response == None:
                            cb_response = dict()
                        # cb_response = json.dumps(cb_response).encode('utf-8')
                        if cb_topic is not None:
                            logger.debug("Invio messaggio {}".format(cb_topic))
                            cb_response = json.dumps(
                                cb_response).encode("utf-8")
                            client.publish(topic=cb_topic, message=cb_response)
                    except Exception as e:
                        logger.warning("Errore CB Serial PUB")
                        logger.debug(
                            "Errore esecuzione callback\n{}".format(e.__str__()))
                    time.sleep(time_wait_after)
        except Exception as e:
            logger.warning("Errore CB Serial PUB")
            logger.debug(
                "Errore esecuzione callback\n{}".format(e.__str__()))
            return
