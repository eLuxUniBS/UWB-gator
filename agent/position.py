import asyncio,json,mqttools, time
import uuid
from datetime import datetime as dt
from agent.skeleton import MQTTAgent, prepare_message
import orm


def format_message_position(*args, val_time: time.time = None,
                            mac_address: str = "AA:AA:AA:AA:AA:AA",
                            x: float = 0.0, y: float = 0.0, z: float = 0.0,
                            q=-1,
                            id_name: str = "TEST000",
                            ts_send: time.time = None,
                            ts_rec: time.time = None, LAST=False, **kwargs) -> \
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
    if buffer.get("time", None) is None:
        buffer["time"] = int(dt.utcnow().timestamp() * 1e6)
    else:
        buffer["time"] = int(buffer["time"])
    if buffer["tags"].get("ts_send", None) is not None:
        buffer["tags"]["ts_send"] = int(buffer["tags"]["ts_send"])
    if buffer["tags"].get("ts_rec", None) is not None:
        buffer["tags"]["ts_rec"] = int(buffer["tags"]["ts_rec"])
    return buffer


def pong(*args, **kwargs):
    print("PONG", args, "\n", kwargs)


def position_refresh(
        topic="", raw={}, header={}, payload={},
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
    try:
        content = orm.dbseries.client.last.read()
        client.publish(topic="/geo", message=json.dumps(prepare_message(
            topic="/geo",payload=content)).encode("UTF-8"),retain=False)
    except Exception as e:
        print(__name__,"Errore in DB", e)


def position_query(topic="", raw={}, header={}, payload={},
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
    # if client is None:
    #     print("Impossibile aggiornare la posizione")
    if payload["query"].strip().lower() == "save":
        save_position(payload["payload"])
    if payload["query"].strip().lower() == "update":
        save_position(payload["payload"])


def save_position(payload):
    """
    Funzione per il salvataggio della posizione
    :param payload:
    :return:
    """
    payload["data"]["fields"]["q"] = float(payload["data"]["fields"]["q"])
    orm.dbseries.client.log.create(**set_message_position(**payload[
        "data"]))
    if payload["data"]["fields"]["mac"] == "MARKER":
        return
    last_copy = payload["data"]
    last_copy["tags"]["ts"] = 0
    last_copy["time"] = 0
    orm.dbseries.client.last.create(**set_message_position(**last_copy))



async def standalone(topic_root="/geo"):
    repeat=True
    client=None
    while True:
        client=await set_client()
        # await client.subscribe(topic=topic_root+'/#')
        await client.subscribe(topic=topic_root+'/ping')
        await client.subscribe(topic=topic_root+'/refresh')
        await client.subscribe(topic=topic_root+'/update')

        while repeat:
            try:
                topic, message = await client.messages.get()
                print("T",topic,"M",message)
                if topic is None and message is None:
                    repeat=False
                if topic is not None and type(topic) is str:
                    topic = topic.strip()
                    # print("TOPIC", topic, time.time())
                    # if topic == topic_root:
                    #     pong(**json.loads(message))
                    if topic == topic_root + "/ping":
                        pong(**json.loads(message))
                    elif topic == topic_root + "/refresh":
                        print("START REFRESH")
                        position_refresh(client=client)
                    elif topic == topic_root + "/update":
                        position_query(**json.loads(message))
                    elif topic.find(topic_root.replace("#", "")) == -1:
                        print("SIDE TOPIC", topic)
                        print(message)
            except Exception as e:
                print("ERRORE IN",e)
        repeat=True
        print("INIZIO DISCONNESSIONE")
        client.disconnect()
        print("DISCONNESSO")

async def set_client(client_id="Position"):
    client = mqttools.Client(client_id=client_id+"_"+uuid.uuid4().__str__(), host="127.0.0.1", port=10008)

    await client.start()
    return client


if __name__=="__main__":
    asyncio.run(standalone())