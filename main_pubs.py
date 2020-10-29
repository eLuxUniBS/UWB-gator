import asyncio
import agent

# TODO caricamento da file YAML
obj_agent = agent.skeleton.MQTTAgent(
    server="localhost",
    port="10008",
    manifest={
        "pubs":{
            "/net/ping":dict(loop=True,wait_seconds=0.5)
        }
    }
)


async def launcher():
    await asyncio.gather(*obj_agent.generate())


if __name__ == "__main__":
    asyncio.run(launcher())
