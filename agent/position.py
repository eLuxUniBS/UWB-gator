import mqttools, time
from datetime import datetime as dt
from agent.skeleton import MQTTAgent
import orm


def format_message_position(*args, val_time: time.time = None,
                            mac_address: str = "AA:AA:AA:AA:AA:AA",
                            x: float = 0.0, y: float = 0.0, z: float = 0.0,
                            q=-1,
                            id_name: str = "TEST000",
                            ts_send: time.time = None,
                            ts_rec: time.time = None, LAST=False,**kwargs) -> \
        dict:
    buffer = dict(time=0 if LAST else int(dt.utcnow().timestamp() * 1e6),
                  fields=dict(mac=mac_address, x=x, y=y, z=z, q=float(q)),
                  tags=dict(
                      id=id_name,
                      ts=0 if LAST else int(dt.utcnow().timestamp() * 1e6)
                  )
                  )
    return set_message_position(**buffer)


def set_message_position(**buffer):
    if buffer.get("time",None) is None:
        buffer["time"]=int(dt.utcnow().timestamp() * 1e6)
    else:
        buffer["time"]=int(buffer["time"])
    if buffer["tags"].get("ts_send", None) is not None:
        buffer["tags"]["ts_send"] = int(buffer["tags"]["ts_send"])
    if buffer["tags"].get("ts_rec", None) is not None:
        buffer["tags"]["ts_rec"] = int(buffer["tags"]["ts_rec"])
    return buffer


async def pong(*args, **kwargs):
    print("PONG", args, "\n", kwargs)


async def position_refresh(topic="", raw={}, header={}, payload={},
                           client: mqttools.Client = None,
                           cb_next_hop: MQTTAgent.publisher = None):
    """
    Aggiorna tutti i subs con le ultime posizioni registrate!
    :param topic:
    :param raw:
    :param header:
    :param payload:
    :param client:
    :param cb_next_hop:
    :return:
    """
    collect_node = dict()
    try:
        content = orm.dbseries.client.last.read()
        await cb_next_hop(topic="/geo", payload=content)
    except Exception as e:
        print("Errore in DB", e)


async def position_update(topic="", raw={}, header={}, payload={},
                          client: mqttools.Client = None,
                          cb_next_hop: MQTTAgent.publisher = None):
    """
    Salva la posizione ricevuta: eventualmente impone un impulso di
    aggiornamento su tutta la rete
    :param topic:
    :param raw:
    :param header:
    :param payload:
    :param client:
    :param cb_next_hop:
    :return:
    """
    if client is None:
        print("Impossibile aggiornare la rete")
    if payload["query"].strip().lower() == "save":
        payload["data"]["fields"]["q"] = float(payload["data"]["fields"]["q"])
        orm.dbseries.client.log.create(**set_message_position(**payload[
            "data"]))
        if payload["data"]["fields"]["mac"] != "MARKER":
            last_copy = payload["data"]
            last_copy["tags"]["ts"] = 0
            last_copy["time"] = 0
            orm.dbseries.client.last.create(**set_message_position(**last_copy))
    position_refresh(cb_next_hop=cb_next_hop)
