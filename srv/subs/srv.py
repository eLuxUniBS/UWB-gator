"""
 +--------+            +--------+            +-------------+
 |        |--- ping -->|        |--- ping -->|             |
 | client |            | broker |            | echo client |
 |        |<-- pong ---|        |<-- pong ---|             |
 +--------+            +--------+            +-------------+
"""
from datetime import datetime as dt
import json
import time
import asyncio
import mqttools

db_ref_last = None
db_ref_log = None
BROKER_PORT = 30000


async def start_client():
    client = mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1])
    await client.start()
    return client


async def response(channel="/buffer", branch=None, test=False):
    """Wait for the client to publish to /ping, and publish /pong in
    response.
    """
    global db_ref_last, db_ref_log
    client = await start_client()
    await client.subscribe(channel)

    while True:
        topic, byte_content = await client.messages.get()
        # print(dt.utcnow(),"TOPIC",topic,"\nCONTENT",byte_content)
        if byte_content is None:
            continue
        try:
            content = json.loads(byte_content.decode('utf-8'))
        except Exception as e:
            print("Errore in codifica messaggio")
            print(byte_content)
            print(e)
            continue
        if test:
            continue
        # DESIGN per spegnere il client
        if topic is None:
            print('Echo client connection lost.')
            break
        if topic.find("/net/refresh") != -1:
            print(content["payload"])
            content["payload"] = db_ref_last.query(content["payload"])
        elif topic.find("/net/update") != -1 or topic.find("/geo/update") != -1:
            print("CONTENT IS ", content["payload"])
            res_to_save = db_ref_last.query(content["payload"])
            db_ref_log.query(content["payload"])
            content["payload"] = res_to_save
        elif topic.find("/collect/position") != -1:
            # print("\nCONTENT COLLECT IS\n",content)
            content["payload"] = db_ref_log.query(content["payload"])
        else:
            content["payload"] = dict(response=202)
        if len(str(content)) > 100:
            message = str(content)[:50] + "..." + str(content)[-50:]
        else:
            message = str(content)
        print(dt.utcnow(), "TOPIC", topic, "\nCONTENT", byte_content, "\nRESP IS", message)
        client.publish("/" + content["header"], json.dumps(content).encode('utf-8'))

        if branch is not None:
            client.publish(branch, json.dumps(content).encode('utf-8'))


async def broker_main():
    """The broker, serving both clients, forever.
    """
    broker = mqttools.Broker(('0.0.0.0', BROKER_PORT))
    await broker.serve_forever()


async def main(orm_last, orm_log):
    global db_ref_last, db_ref_log
    db_ref_last = orm_last
    db_ref_log = orm_log
    await asyncio.gather(
        response(channel="/net"),
        response(channel="/net/refresh"),
        response(channel="/net/update"),
        response(channel="/collect/position")
    )
