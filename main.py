import click
import asyncio
import orm
from srv.subs.srv import main as main_subs
from srv.pubs.client import main as main_pubs

def launch_cli_server(localhost:str=None,port:int=None):
    asyncio.run(main_subs(orm_last=orm.dbseries.client.last,
                          orm_log=orm.dbseries.client.log,localhost=localhost,port=port))


def launch_cli_client():
    asyncio.run(main_pubs())


@click.command()
@click.option("--mode", default="cli_server", help="""Usa una delle seguenti modalità:
\nserver\tlancio servizio (default)
\ncli_server\tserver da linea di comando
\ncli_client\tclient da linea di comando""")
@click.option("--host", default="localhost", help="MQTT Broker host")
@click.option("--port", default="1883", help="MQTT Broker port")
def launch(mode,host,port):
    try:
        mode = mode.lower().strip()
        host=host.strip()
        port=int(port)
    except Exception as e:
        print("Errore nei parametri di ingresso",e)
        exit()
    if mode == "cli_client":
        launch_cli_client()
    else:
        launch_cli_server(localhost=host,port=int(port))


if __name__ == "__main__":
    launch()
