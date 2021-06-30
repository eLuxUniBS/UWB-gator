import argparse
import asyncio
import srv

def launch(mode, host, port, *args, **kwargs):
    try:
        mode = mode.lower().strip()
        host = host.strip()
        port = int(port)
    except Exception as e:
        print("Errore nei parametri di ingresso", e)
        exit()
    if mode == "cli_client":
        launch_cli_client(localhost=host, port=int(port),
                          kind_app="mobile_app")
    elif mode == "cli_client_serial":
        launch_cli_client(localhost=host, port=int(port), kind_app="vehicle")
    elif mode == "cli_client_test_net":
        launch_cli_client(localhost=host, port=int(port), kind_app="test_net")
    elif mode == "cli_client_monitor":
        launch_cli_client(localhost=host, port=int(port), kind_app="monitor")
    elif mode == "cli_server":
        launch_cli_server(localhost=host, port=int(port))
    elif mode == "cli_server_monitor":
        launch_cli_server(localhost=host, port=int(port), kind_app="monitor")
    else:
        print("Opzione non prevista")
        exit(2)


def option():
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
                        choices=["cli_client", "cli_client_serial", "cli_client_test_net", "cli_client_monitor", "cli_server", "cli_server_monitor"], 
                        dest="mode", 
                        default="cli_server"
                        )
    opt = parser.parse_args()
    return opt.__dict__


if __name__ == "__main__":
    opts = option()
    launch(**opts)
