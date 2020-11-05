import asyncio, argparse, time
import json
from math import cos,pi,sin

import mqttools

from agent.position import standalone, set_client


async def loop_move():
    def prepare_message(x,y,mac,id,z=0,q=100):
        return dict(header="id",
                   payload=dict(
                       query="save",
                       payload=dict(
                           data=dict(
                               fields=dict(
                                   mac=mac,
                                   x=float(x),
                                   y=float(y),
                                   z=float(0),
                               q=float(100)),
                           tags=dict(id=id,ts=time.time()*1000*1000)))))

    client = await set_client(client_id="Move")
    index=0
    while True:
        x = y = 0
        for _ in range(0,100):
            for node in [
                dict(id="DWD537",mac="c6:d6:37:d1:08:42",mode="linear"),
                dict(id="DW0B09",mac="D3:A8:C9:E3:9A:5A",mode="inverse_circular"),
                dict(id="DW4836",mac="D6:CC:4C:D7:7C:AF",mode="circular")
            ]:
                x+=1
                y+=1
                index+=1
                if node["mode"]=="linear":
                    message = prepare_message(x*50,y*50,id=node["id"],mac=node["mac"].upper())
                elif node["mode"]=="circular":
                    message = prepare_message(cos(index/500*pi)*5000,sin(index/500*pi)*5000,id=node["id"],mac=node["mac"])
                elif node["mode"]=="inverse_circular":
                    message = prepare_message(-cos(index/500*pi)*10000,-sin(index/500*pi)*10000,id=node["id"],mac=node["mac"])
                if index>=1000:
                    index=0
                if(x>=50):
                    x=0
                if(y>=75):
                    y=-25
                client.publish("/geo/update", message=json.dumps(message).encode("UTF-8"))
            time.sleep(0.25)


async def loop_pub():
    client = await set_client(client_id="Loop")
    while True:
        try:
            print(client.client_id, "SEND", time.time())
            client.publish('/geo/refresh', b'{}', retain=False)
            time.sleep(0.05)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Worker dedito all posizione geografica")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--worker", type=str, default=None, choices=["loop", "move"])
    args = parser.parse_args()
    if args.worker is None:
        asyncio.run(standalone())
    elif args.worker.find("loop") != -1:
        asyncio.run(loop_pub())
    elif args.worker.find("move") != -1:
        asyncio.run(loop_move())
