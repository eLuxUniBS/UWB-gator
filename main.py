import click
import asyncio
from orm import dbseries as orm
from srv.subs.srv import main as main_subs
from srv.pubs.client import main as main_pubs
# TODO
# from server import launcher as main_server

def launch_cli_server():
    db_name = "eseb"
    db_table = "last"
    token="IJD9EtstUEQgUQgluW0I4LkwLpQLh0n5EP02zIerYS98_Q0EA4trRX_TBxDx1pt7heusiQ6TgDjX3EAaPMQXww=="
    db_obj = orm.DB(token,db_name=db_name, db_table=db_table)
    # db_obj.create_db()
    asyncio.run(main_subs(db_obj))


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
