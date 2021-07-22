"""
 +--------+            +--------+            +-------------+
 |        |--- ping -->|        |--- ping -->|             |
 | client |            | broker |            | echo client |
 |        |<-- pong ---|        |<-- pong ---|             |
 +--------+            +--------+            +-------------+
"""
from datetime import datetime as dt
import json,time,asyncio,mqttools,logging
logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

db_ref_last = None
db_ref_log = None
db_ref_gen=None
BROKER_PORT = 30000
BROKER_HOST = "10.211.55.28"


async def start_client(localhost: str = None, port: int = None):
    if localhost is None:
        localhost = BROKER_HOST
    if port is None:
        port = BROKER_PORT
    client = mqttools.Client(localhost, port, connect_delays=[0.1])
    await client.start()
    return client


async def response(channel="/buffer", branch=None, test=False, localhost=None, port=None):
    """Wait for the client to publish to /ping, and publish /pong in
    response.
    """
    global db_ref_last, db_ref_log,db_ref_gen
    logger.debug(f'channel')
    client = await start_client(localhost=localhost, port=port)
    await client.subscribe(channel)
    while True:
        topic, byte_content = await client.messages.get()
        if byte_content is None:
            continue
        try:
            content=byte_content.decode('utf-8')
            logger.debug(f'content')
            content = json.loads(content)
        except Exception as e:
            logger.debug(f'e')
            continue
        if test:
            continue
        # DESIGN per spegnere il client
        if topic is None:
            print('Echo client connection lost.')
            continue
        try:
            if topic.find("/net/refresh") != -1:
                content["payload"] = db_ref_last.query(content["payload"])
            elif topic.find("/net/update") != -1 or topic.find("/geo/update") != -1:                
                res_to_save = db_ref_last.query(content["payload"])
                db_ref_log.query(content["payload"])
                content["payload"] = res_to_save
            elif topic.find("/net/archive") != -1:
                dataset = content["payload"].get("data", {})
                if type(dataset) is str:
                    dataset = json.loads(dataset)
                    dataset = dataset.get("data_sendit", {})
                for single_data in [json.loads(x) for x in dataset]:
                    if single_data.get("obj", None) is None:
                        continue
                    temp = json.loads(single_data.get("obj"))
                    if temp.get("payload", None) is None:
                        logger.info("Payload assente per {}".format(topic))
                        continue
                    if temp["payload"].get("data", None) is None:
                        prepare_data_to_save = dict(
                            query=content["payload"].get("query", None),
                            data=temp["payload"]
                        )
                    else:
                        prepare_data_to_save = dict(
                            query=content["payload"].get("query", None),
                            data=temp["payload"].get("data", {})
                        )
                    db_ref_log.query(prepare_data_to_save)
                    prepare_data_to_save["data"]["tags"]["ts"] = 0
                    prepare_data_to_save["data"]["time"] = 0
                    res_to_save = db_ref_last.query(prepare_data_to_save)
                    # content["payload"] = res_to_save
            elif topic.find("/collect/position") != -1:
                # print("\nCONTENT COLLECT IS\n",content)
                content["payload"] = db_ref_log.query(content["payload"])
            elif topic.find("/p2p/data") != -1:                
                if db_ref_gen is not None:
                    db_ref_gen.RawSignal.create(header=content["header"],body=content["payload"])                
                else:
                    print("Impossibile salvare")
                continue
            else:
                content["payload"] = dict(response=202)
            if len(str(content)) > 100:
                message = str(content)[:50] + "..." + str(content)[-50:]
            else:
                message = str(content)
            logger.debug("{} TOPIC {}\nCONTENT{}\nRESPONSE IS\t {}".format(dt.utcnow(), topic,byte_content, message))
            if branch is not None:
                client.publish(branch, json.dumps(content).encode('utf-8'))
            elif type(content.get("header",None)) is str:
                client.publish("/" + content["header"],
                            json.dumps(content).encode('utf-8'))
            elif content.get("header").get("next_hop",None) is not None:
                client.publish("/" + content["header"]["next_hop"],
                            json.dumps(content).encode('utf-8'))            
        except Exception as e:
            print("Errore ", e)


async def broker_main():
    """The broker, serving both clients, forever.
    """
    broker = mqttools.Broker((BROKER_HOST, BROKER_PORT))
    await broker.serve_forever()


async def main(orm_last, orm_log, localhost=None, port=None, orm_gen=None,kind_app:str=None):
    global db_ref_last, db_ref_log, db_ref_gen
    db_ref_last = orm_last
    db_ref_log = orm_log
    if orm_gen is not None:
        db_ref_gen = orm_gen
    if kind_app=="monitor":
        await asyncio.gather(
        response(channel="/net/refresh",branch="/net", localhost=localhost, port=port),
    )
    else:
        await asyncio.gather(
            response(channel="/net", localhost=localhost, port=port),
            response(channel="/net/refresh", localhost=localhost, port=port),
            response(channel="/net/update", localhost=localhost, port=port),
            response(channel="/net/archive",
                    localhost=localhost, port=port),  # Metering
            response(channel="/collect/position", localhost=localhost, port=port),
            response(channel="/p2p/data", localhost=localhost, port=port),
        )
