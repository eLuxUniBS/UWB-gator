import asyncio
import json
import time
from datetime import datetime as dt

import mqttools

BROKER_PORT = 10008


async def test_publisher():
    async with mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1]) as client:
        await client.subscribe('/node_01')
        message = dict(header='node_01', payload=dict(query="save", data=dict(
            fields=dict(mac="FF:FF:FF:FF:FF:FF",
                        x=0.0,
                        y=0.0,
                        z=0.0,
                        q=100.0),
            tags=dict(
                id="DWBETA",
                ts=int(time.time()),
            )
        )))
        client.publish('/buffer', json.dumps(message).encode('utf-8'))
        topic, byte_content = await client.messages.get()
        message=json.loads(byte_content.decode('utf-8'))
        print(f'client: Got {byte_content} on {topic}.')
        if message["payload"].get("response",None)!= 200:
            print("ERRORE")
            return None
        message = dict(header='node_01', payload=dict(query="get", data=dict(
            measurement="positions_register"
        )))
        client.publish('/buffer', json.dumps(message).encode('utf-8'))
        topic, message = await client.messages.get()
        print("MESSAGE RECEIVED",message,topic)



async def pubsMonitor():
    async with mqttools.Client('localhost', BROKER_PORT, connect_delays=[0.1]) as client:
        await client.subscribe('/routine')
        message = dict(header='monitor', payload=dict(query="get", data=dict(
            measurement="positions_register"
        )))
        client.publish('/net', json.dumps(message).encode('utf-8'))
        topic, message = await client.messages.get()
        print("MESSAGE RECEIVED",message,topic)


asyncio.run(test_publisher())
