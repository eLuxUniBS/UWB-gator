
import logging,json
from datetime import datetime as dt
from typing import Callable

import mqttools

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def ping(*args,input_message:dict=None, **kwargs)->tuple:
    """
    Funzionalità di ping per il test della comunicazione
    """
    log.debug("PING{ts} con messaggio {input_message}\n Altri parametri\n args={args} kwargs={kwargs}".format(        
        ts=dt.utcnow().__str__(),
        input_message=input_message,
        args=",".join(args),
        kwargs=",".join(["{}:{}".format(k,kwargs.get(x,"-missing-").__str__) for k in kwargs.keys()]))
        )
    return None,None


async def wrapper_callback_sub(*args, cb: Callable = ping, channel: str = None, host: str = None, port: int = None, connection_delays: list = None, turn_off_with_empty_topic:bool=False,topic_response: str = None, **kwargs):
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
    connection_delays = connection_delays if connection_delays is not None and len(connection_delays)>0 and type(connection_delays[0])==float else [0.1]
    # Avvio servizio
    client = mqttools.Client(host=host, port=port, connect_delays=[0.1])
    await client.start()
    await client.subscribe(channel)
    while True:
        topic, byte_content = await client.messages.get()
        if byte_content is None:
            log.warning("Messaggio vuoto per topic {}".format(topic))
            continue
        try:
            content = json.loads(byte_content.decode('utf-8'))
        except Exception as e:
            log.warning("Errore decodifica json content utf8")
            log.debug("Errore\n{}".format(e.__str__()))
            continue
        if topic is None and turn_off_with_empty_topic:
            log.info("Chiusura topic")
            return
        try:
            cb_topic,cb_response=cb(*args,input_message=content,**kwargs)
            if cb_topic is None:
                cb_topic=topic_response                                   
            if cb_topic is not None:
                log.debug("Emissione messaggio dal canale {} con topic {}".format(channel,cb_topic))
                response=json.dumps(cb_response).encode('utf-8')
                await client.publish(topic=cb_topic,message=response)
        except Exception as e:
            log.warning("Errore CB")
            log.debug("Errore esecuzione callback\n{}".format(e.__str__()))
            continue
        


async def wrapper_callback_pub(*args, cb: Callable = ping, channel: str = None, host: str = None, port: int = None, connection_delays: list = None, topic_response: str = None, **kwargs):
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
    connection_delays = connection_delays if connection_delays is not None and len(connection_delays)>0 and type(connection_delays[0])==float else [0.1]
    # Avvio servizio
    client = mqttools.Client(host=host, port=port, connect_delays=[0.1])
    await client.start()
    await client.subscribe(channel)
    while True:        
        try:
            cb_topic,cb_response=cb(*args,**kwargs)
            if cb_topic is None:
                cb_topic=topic_response
            response=json.dumps(cb_response).encode('utf-8')
            await client.publish(topic=cb_topic,message=response)
        except Exception as e:
            log.warning("Errore CB")
            log.debug("Errore esecuzione callback\n{}".format(e.__str__()))
            continue
        