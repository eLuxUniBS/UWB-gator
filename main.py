import click
import asyncio
import orm
from srv.subs.srv import main as main_subs
from srv.pubs.client import main as main_pubs


# TODO
# from server import launcher as main_server

def launch_cli_server():
    asyncio.run(main_subs(orm_last=orm.dbseries.client.last,
                          orm_log=orm.dbseries.client.log))


def launch_cli_client():
    asyncio.run(main_pubs())


def launch_server():
    pass
    # main_server.launcher()


@click.command()
@click.option("--mode", default="server", help="""Usa una delle seguenti modalità:
\nserver\tlancio servizio (default)
\ncli_server\tserver da linea di comando
\ncli_client\tclient da linea di comando""")
def launch(mode):
    mode = mode.lower().strip()
    if mode == "server":
        launch_server()
    elif mode == "cli_server":
        launch_cli_server()
    elif mode == "cli_client":
        launch_cli_client()


if __name__ == "__main__":
    launch()
