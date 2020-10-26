import asyncio
import agent

single_agent = agent.skeleton.MQTTAgent(server="0.0.0.0",
                                        port="10008",
                                        manifest={
                                            "/net/ping": agent.network.pong,
                                            "/net/refresh":
                                                agent.network.network_refresh,
                                            "/net/update":
                                                agent.network.pong,
                                            "/geo/ping": agent.position.pong,
                                            "/geo/refresh": agent.position.position_refresh,
                                            "/geo/update": agent.position.position_update
                                        })


async def launcher():
    await asyncio.gather(*single_agent.generate_subscriber())


if __name__ == "__main__":
    asyncio.run(launcher())
