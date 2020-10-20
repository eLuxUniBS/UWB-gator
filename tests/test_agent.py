import asyncio
import agent

single_agent = agent.skeleton.MQTTAgent(server="localhost",
                                        port="10008",
                                        manifest={
                                            "/net/ping": agent.network.pong,
                                            "/net/refresh":
                                                agent.network.network_refresh,
                                            "/net/update":
                                                agent.network.pong
                                        })


async def launcher():
    await asyncio.gather(*single_agent.generate_subscriber())


if __name__ == "__main__":
    asyncio.run(launcher())
