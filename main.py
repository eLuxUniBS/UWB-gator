import click
import asyncio
import orm
from srv.subs.srv import main as main_subs
from srv.pubs.client import main as main_pubs

def launch_cli_server(localhost:str=None,port:int=None,kind_app:str=None):
    asyncio.run(main_subs(orm_last=orm.dbseries.client.last,
                          orm_log=orm.dbseries.client.log,
                          orm_gen=orm.db,
                          localhost=localhost,port=port,kind_app=kind_app))


def launch_cli_client(*args,kind_app:str=None,**kwargs):
    asyncio.run(main_pubs(*args,kind_app=kind_app,**kwargs))


@click.command()
@click.option("--mode", default="cli_server", help="""Usa una delle seguenti modalità:
\nserver\tlancio servizio (default)
\ncli_server\tserver da linea di comando
\ncli_server_monitor\tserver da linea di comando
\ncli_client\tclient da linea di comando
\ncli_client_serial\tclient da linea di comando per la porta seriale""")
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
        launch_cli_client(localhost=host,port=int(port),kind_app="mobile_app")
    elif mode == "cli_client_serial":
        launch_cli_client(localhost=host,port=int(port),kind_app="vehicle")
    elif mode == "cli_client_test_net":
        launch_cli_client(localhost=host,port=int(port),kind_app="test_net")
    elif mode == "cli_client_monitor":
        launch_cli_client(localhost=host,port=int(port),kind_app="monitor")
    elif mode == "cli_server_monitor":
        launch_cli_server(localhost=host,port=int(port),kind_app="monitor")
    else:
        launch_cli_server(localhost=host,port=int(port))


if __name__ == "__main__":
    launch()
