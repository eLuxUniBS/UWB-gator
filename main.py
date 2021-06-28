import argparse
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


# @click.option("--host", default="localhost", help="MQTT Broker host")
# @click.option("--port", default="1883", help="MQTT Broker port")
def launch(mode,host,port,*args,**kwargs):
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
    elif mode =="cli_server":
        launch_cli_server(localhost=host,port=int(port))
    elif mode == "cli_server_monitor":
        launch_cli_server(localhost=host,port=int(port),kind_app="monitor")
    else:
        print("Opzione non valida")
        exit(2)


def option():
    parser=argparse.ArgumentParser(add_help="Differenti Modalità di lancio")
    parser.add_argument('-p','--port',help="Porta di accesso al broker mqtt",default="1883",dest="port")
    parser.add_argument('-i','--ip',help="Host di accesso al broker mqtt",default="localhost",dest="host")
    parser.add_argument('-m','--mode',choices=["cli_client","cli_client_serial","cli_client_test_net","cli_client_monitor","cli_server","cli_server_monitor"],dest="mode",default="cli_server")
    opt= parser.parse_args()
    return opt.__dict__

if __name__ == "__main__":
    opts=option()
    launch(**opts)
