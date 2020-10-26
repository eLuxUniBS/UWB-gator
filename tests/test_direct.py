import asyncio
from agent.skeleton import MQTTAgent

agent = MQTTAgent(server="192.168.0.2", port="10008")


async def test_pubs():
    await agent.publisher(topic="/net/ping", payload={"message": "net ping"})
    await agent.publisher(topic="/geo/ping", payload={"message": "geo ping"})


async def retrieve_net_config():
    await agent.publisher(topic="/net/refresh")
    await agent.publisher(topic="/geo/refresh")


async def modify_network():
    await agent.publisher(topic="/net/refresh", payload={"message": "ping"})
    await agent.publisher(topic="/net/update", payload={"message": "ping"})

async def modify_position():
    await agent.publisher(topic="/geo/refresh", payload={"message": "ping"})
    await agent.publisher(topic="/geo/update", payload={"message": "ping"})


async def loop():
    await asyncio.gather(*[
        test_pubs(),
        retrieve_net_config()
    ])


if __name__ == "__main__":
    asyncio.run(loop())
