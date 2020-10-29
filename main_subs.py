import asyncio
import agent

# TODO caricamento da file YAML
obj_agent = agent.skeleton.MQTTAgent(
    server="localhost",
    port="10008",
    manifest={
        "subs": {
            "/net/ping": dict(core=agent.network.pong),
            "/net/refresh": dict(core=agent.network.network_refresh),
            "/net/update": dict(core=agent.network.network_query),
            "/geo/ping": dict(core=agent.position.pong),
            "/geo/refresh": dict(core=agent.position.position_refresh),
            "/geo/update": dict(core=agent.position.position_query),
        }
    }
)


async def launcher():
    await asyncio.gather(*obj_agent.generate())


if __name__ == "__main__":
    asyncio.run(launcher())
