import asyncio
import json
import time
import math
from datetime import datetime as dt, timedelta

import mqttools

BROKER_PORT = 1883


async def prepareFields(subs: str = "routine_preapare_fields", server="localhost", port=BROKER_PORT):
    async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
        await client.subscribe("/" + subs)
        for data in [
            dict(
                fields=dict(mac="EB:61:5E:75:4A:44", x=1400.0,
                            y=0.0, z=1300.0, q=100.0),
                tags=dict(id="DW9424", ts=int(time.time()))
            ),
            dict(
                fields=dict(mac="EE:C9:20:24:B6:3F", x=1400.0,
                            y=4400.0, z=900.0, q=100.0),
                tags=dict(id="DWC327", ts=int(time.time()))
            ),
            dict(
                fields=dict(mac="CF:62:E0:96:1F:45", x=2500.0,
                            y=3750.0, z=1900.0, q=100.0),
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
            response = client.publish(
                topic, json.dumps(message).encode('utf-8'))
            print(dt.utcnow(), "write to {} --- this message".format(topic),
                  "\nMessage", message, "\nResponse", response)
            time.sleep(0.2)


async def ping(time_before: timedelta = None, time_after: timedelta = None, server="localhost", port=BROKER_PORT, topic="/net/refresh"):
    if time_before is None:
        time_before = timedelta(seconds=0)
    time_before = time_before.total_seconds()
    if time_after is None:
        time_after = timedelta(seconds=0.2)
    time_after = time_after.total_seconds()
    while True:
        message = dict(payload=dict(query="get"))
        async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
            time.sleep(time_before)
            response = client.publish(
                topic, json.dumps(message).encode('utf-8'))
            print(dt.utcnow(), "write to {} --- this message".format(topic),
                  "\nMessage", message, "\nResponse", response)
            time.sleep(time_after)


async def test_net(time_before: timedelta = None, time_after: timedelta = None, server="localhost", port=BROKER_PORT, topic="/net", nodes: list = None):
    if time_before is None:
        time_before = timedelta(seconds=0)
    time_before = time_before.total_seconds()
    if time_after is None:
        time_after = timedelta(seconds=0.05)
    time_after = time_after.total_seconds()
    if nodes is None:
        return
    counter = 0
    step = 5000
    max_step = 1000000
    ray = 10000
    step_ray = 1
    while True:
        message = []
        for x in nodes:
            message.append(x.copy())
            if x["x"] == x["y"] == x["z"] == 0:
                next_step=(counter/max_step)*2*math.pi*step_ray
                message[-1]["x"] = math.cos(next_step)*ray
                message[-1]["y"] = math.sin(next_step)*ray
                message[-1]["z"] = math.tan(next_step)*ray
            elif x["x"] == x["y"] == x["z"] == -1:          
                next_step=(counter/max_step)* 2*math.pi*(-step_ray)
                message[-1]["x"] = math.cos(next_step)*ray
                message[-1]["y"] = math.sin(next_step)*ray
                message[-1]["z"] = math.tan(next_step)*ray
        counter += step
        if counter >= max_step:
            counter = 0
            step_ray *= -1
        async with mqttools.Client(server, port, connect_delays=[0.1]) as client:
            time.sleep(time_before)
            values = []
            columns = list(message[-1].keys())
            for row in message:
                values.append([])
                for label in row.keys():
                    values[-1].append(row[label])
            data = dict(series=[dict(
                columns=columns,
                values=values
            )])
            response = client.publish(topic, json.dumps(dict(header="", payload=dict(
                data=data))).encode('utf-8'))
            print(dt.utcnow(), "write to {} --- this message".format(topic),
                  "\nMessage", message, "\nResponse", response)
            time.sleep(time_after)
