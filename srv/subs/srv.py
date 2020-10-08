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


db_ref = None
BROKER_PORT = 10008


async def start_client():
    client = mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1])
    await client.start()
    return client


async def response(channel="/buffer", branch=None, test=False):
    """Wait for the client to publish to /ping, and publish /pong in
    response.
    """
    global db_ref
    client = await start_client()
    await client.subscribe(channel)

    while True:
        topic, byte_content = await client.messages.get()
        if byte_content is None:
            continue
        try:
            content = json.loads(byte_content.decode('utf-8'))
        except Exception as e:
            print("Errore in codifica messaggio")
            print(byte_content)
            print(e)
            continue
        print(f'{dt.now()} Client: Got {content} on {topic}.')
        if test:
            continue
        # DESIGN per spegnere il client
        # if topic is None:
        #     print('Echo client connection lost.')
        #     break
        print("CHANNEL",channel)
        if channel.find("/net/refresh")!=-1 or channel.find("/net/update")!=-1:
            content["payload"] = db_ref.query(content["payload"])
            print("CONTENT REFRESH UPDATE IS\n",content)
        elif channel.find("/collect/position")!=-1:
            print("CONTENT COLLECT IS\n",content)
            content["payload"] = db_ref.query(content["payload"])
        else:
            content["payload"] = dict(response=202)
        #print("RESP IS",content)
        client.publish("/" + content["header"], json.dumps(content).encode('utf-8'))

        if branch is not None:
            client.publish(branch, json.dumps(content).encode('utf-8'))


async def broker_main():
    """The broker, serving both clients, forever.
    """
    broker = mqttools.Broker(('0.0.0.0', BROKER_PORT))
    await broker.serve_forever()


async def main(orm):
    global db_ref
    db_ref = orm
    await asyncio.gather(
        response(channel="/buffer", branch="/test"),
        response(channel="/net"),
        response(channel="/net/refresh"),
        response(channel="/net/update"),
        response(channel="/collect/position"),
        response(channel="/test", test=True)
    )