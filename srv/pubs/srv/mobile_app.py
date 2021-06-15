import asyncio
import json
import time
from datetime import datetime as dt

import mqttools

BROKER_PORT = 30000


async def prepareFields(subs: str = "routine_preapare_fields", server="localhost", port=BROKER_PORT):
    async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
        await client.subscribe("/" + subs)
        for data in [
            dict(
                fields=dict(mac="EB:61:5E:75:4A:44", x=1400.0, y=0.0, z=1300.0, q=100.0),
                tags=dict(id="DW9424", ts=int(time.time()))
            ),
            dict(
                fields=dict(mac="EE:C9:20:24:B6:3F", x=1400.0, y=4400.0, z=900.0, q=100.0),
                tags=dict(id="DWC327", ts=int(time.time()))
            ),
            dict(
                fields=dict(mac="CF:62:E0:96:1F:45", x=2500.0, y=3750.0, z=1900.0, q=100.0),
                tags=dict(id="DW5628", ts=int(time.time()))
            ),
        ]:
            message = dict(header=subs, payload=dict(query="save", data=data))
            client.publish('/net/update', json.dumps(message).encode('utf-8'))


async def pubsMonitor(subs: str = "net/geo", server="localhost", port=BROKER_PORT, topic="/net/refresh"):
    while True:
        async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
            await client.subscribe("/" + subs)
            message = dict(
                header=subs,
                payload=dict(
                    query="get"
                )
            )
            response = client.publish(topic, json.dumps(message).encode('utf-8'))
            print(dt.utcnow(), "write to {} --- this message".format(topic), "\nMessage",message,"\nResponse",response)
            time.sleep(0.2)
