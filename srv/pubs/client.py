import asyncio

from .srv import prepareFields, pubsMonitor


BROKER_PORT = 10008
async def main(localhost="localhost",port=BROKER_PORT):
    await asyncio.gather(
        prepareFields(server=localhost, port=port),
        pubsMonitor(server=localhost, port=port)
    )

if __name__ == "__main__":
    asyncio.run(main())
