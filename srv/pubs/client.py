import asyncio

from .srv import mobile_app, vehicle


BROKER_PORT = 30000


async def main(localhost="10.42.0.72", port=BROKER_PORT, kind_app="mobile_app"):
    if kind_app == "mobile_app":
        await asyncio.gather(
            mobile_app.prepareFields(server=localhost, port=port),
            mobile_app.pubsMonitor(server=localhost, port=port)
        )
    elif kind_app == "vehicle":
        paths = [
            ("idA","/dev/serial/by-id/usb-SEGGER_J-Link_000760029246-if00"),
            ("idB","/dev/serial/by-id/usb-SEGGER_J-Link_000760029217-if00"),
#            ("idC","/dev/serial/by-id/usb-SEGGER_J-Link_000760029214-if00")
        ]
        await asyncio.gather(
            *[vehicle.pubMeasurementFromSerial(
                server=localhost,
                port=port,
                serial_path=path,
                id_send=id,
                baudrate=115200,
                timeout=0.5
            ) for (id,path) in paths]
        )
    elif kind_app=="monitor":        
        await asyncio.gather(
            mobile_app.ping(server=localhost, port=port)
        )
    elif kind_app=="test_net":      
        await asyncio.gather(
            mobile_app.test_net(server=localhost, port=port,nodes=[
                dict(mac="c6:d6:37:d1:08:42",id="DWD537",x=0,y=0,z=0,q=100),
                dict(mac="e3:3a:13:b2:5f:56",id="DW8615",x=-1,y=-1,z=-1,q=100),
                # dict(mac="",id="",x=0,y=0,z=0,q=100),
                # dict(mac="",id="",x=0,y=0,z=0,q=100)
                ])
        )
    else:
        pass

if __name__ == "__main__":
    asyncio.run(main())
