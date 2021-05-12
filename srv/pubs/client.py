import asyncio

from .srv import prepareFields, pubsMonitor


BROKER_PORT = 30000
async def main(localhost="10.42.0.72",port=BROKER_PORT):
    await asyncio.gather(
        prepareFields(server=localhost, port=port),
        pubsMonitor(server=localhost, port=port)
    )

if __name__ == "__main__":
    asyncio.run(main())
