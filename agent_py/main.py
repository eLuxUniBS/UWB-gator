import argparse,asyncio
from enum import Enum
from datetime import datetime as dt
from srv.wrapper import wrapper_callback_sub, wrapper_callback_pub, ping
from srv import db


async def launcher(list_cb: list):
    await asyncio.gather(*list_cb)


def launch_cli_client(list_cb: list):
    asyncio.run(launcher(list_cb=list_cb))


class CMDOptions(Enum):
    pub_ping_test= "pub_ping_test"
    sub_ping_test= "sub_ping_test"
    pub_serial= "pub_serial"
    pub_update_net= "pub_update_net"
    sub_db= "sub_db"


def launch(mode, host, port, *args, **kwargs):
    try:
        mode = mode.lower().strip()
        host = host.strip()
        port = int(port)
        mode=[single for single in CMDOptions if single.value==mode][0]
    except Exception as e:
        print("Errore nei parametri di ingresso", e)
        exit()
    if mode == CMDOptions.pub_update_net:
        pass
        # launch_cli_client(localhost=host, port=int(port),
        #                   kind_app="mobile_app")
    elif mode == CMDOptions.sub_db:
        #TODO verifica possibilità di avere due db reader/writer sullo stesso async
        launch_cli_client([wrapper_callback_pub(
            channel="/db_serial", cb=db.influxdb, mark_ts=str(dt.utcnow()))])
    elif mode == CMDOptions.pub_ping_test:
        launch_cli_client([wrapper_callback_pub(
            channel="/ping", cb=ping, mark_ts=str(dt.utcnow()))])
    elif mode == CMDOptions.sub_ping_test:
        launch_cli_client([wrapper_callback_sub(
            channel="/ping", cb=ping, mark_ts=str(dt.utcnow()))])
    else:
        print("Opzione non prevista")
        exit(2)


def option():
    # choices = ["cli_client", "cli_client_serial", "cli_client_test_net", "cli_client_monitor",
    #            "cli_server", "cli_server_monitor", "test_ping_pub", "test_ping_sub"]
    choices = [k.value for k in CMDOptions]
    parser = argparse.ArgumentParser(add_help="Differenti Modalità di lancio")
    parser.add_argument(
        '-p', '--port',
        help="Porta di accesso al broker mqtt",
        default="1883",
        dest="port"
    )
    parser.add_argument(
        '-i', '--ip',
        help="Host di accesso al broker mqtt",
        default="localhost",
        dest="host"
    )
    parser.add_argument('-m', '--mode',
                        choices=choices,
                        dest="mode",
                        default="-missing-"
                        )
    opt = parser.parse_args()
    return opt.__dict__


if __name__ == "__main__":
    opts = option()
    launch(**opts)
