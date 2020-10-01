import asyncio

from srv import prepareFields, pubsMonitor


BROKER_PORT = 10008
async def main():
    await asyncio.gather(
        prepareFields(server="localhost", port=BROKER_PORT),
        pubsMonitor(server="localhost", port=BROKER_PORT)
    )

if __name__ == "__main__":
    asyncio.run(main())
