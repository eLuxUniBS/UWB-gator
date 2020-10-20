import mqttools, time
from datetime import datetime as dt
from agent.skeleton import MQTTAgent
import orm


def format_message_position(*args, val_time: time.time = None,
                            mac_address: str = "AA:AA:AA:AA:AA:AA",
                            x: float = 0.0, y: float = 0.0, z: float = 0.0,
                            q: int = -1,
                            id_name: str = "TEST000",
                            ts_send: time.time = None,
                            ts_rec: time.time = None, **kwargs) -> dict:
    buffer = dict(
        fields=dict(mac=mac_address, x=x, y=y, z=z, q=q),
        tags=dict(id=id_name, ts_rec=int(dt.utcnow().timestamp() * 1e6)))
    if val_time is not None:
        buffer["time"] = int(val_time)
    if ts_send is not None:
        buffer["tags"]["ts_send"] = int(ts_send)
    if ts_rec is not None:
        buffer["tags"]["ts_rec"] = int(ts_rec)
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
    if payload.get("refresh_position", None) is not None:
        await cb_next_hop(topic="/geo/refresh", payload={
            "message":
                "Ricevuto {}#{} alle {}, e rinviato alle {}".format(
                    header.get("name", "-missing-"),
                    header.get("uuid", "-missing-"),
                    header.get("ts", "-missing-"),
                    dt.utcnow().__str__())})
