import asyncio
import agent

# TODO caricamento da file YAML
geo_refresh = agent.skeleton.MQTTAgent(
    server="localhost",
    port="10008",
    manifest={
        "pubs": {
            "/geo/refresh": dict(loop=True, wait_seconds=0.1),

        }
    }
)
net_refresh = agent.skeleton.MQTTAgent(
    server="localhost",
    port="10008",
    manifest={
        "pubs": {
            "/net/refresh": dict(loop=True, wait_seconds=1),

        }
    }
)


async def launcher():
    await asyncio.gather(*[
        *geo_refresh.generate_publisher(),
        # *net_refresh.generate_publisher()
    ])


if __name__ == "__main__":
    asyncio.run(launcher())
