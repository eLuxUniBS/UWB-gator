"""
 +--------+            +--------+            +-------------+
 |        |--- ping -->|        |--- ping -->|             |
 | client |            | broker |            | echo client |
 |        |<-- pong ---|        |<-- pong ---|             |
 +--------+            +--------+            +-------------+
"""
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
    global  db_ref
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
        print(f'echo_client: Got {content} on {topic}.')
        if test:
            continue
        #
        # if topic is None:
        #     print('Echo client connection lost.')
        #     break
        response=db_ref.query(content["payload"])
        content["payload"]=response
        client.publish("/" + content["header"], json.dumps(content).encode('utf-8'))

        if branch is not None:
            client.publish(branch, json.dumps(content).encode('utf-8'))


async def broker_main():
    """The broker, serving both clients, forever.
    """
    broker = mqttools.Broker(('localhost', BROKER_PORT))
    await broker.serve_forever()


async def main(orm):
    global db_ref
    db_ref = orm
    await asyncio.gather(
        broker_main(),
        response(channel="/buffer", branch="/test"),
        response(channel="/test", test=True)
    )
