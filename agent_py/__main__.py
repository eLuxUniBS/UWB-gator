import argparse
import asyncio
from enum import Enum
from datetime import datetime as dt

import serial
from agent_py.srv.wrapper import wrapper_callback_sub, wrapper_callback_pub, ping, wrapper_serial_callback_pub
from agent_py.srv import orm, pubs, subs


sample_nodes = [
    dict(
        mac="c6:d6:37:d1:08:42", id="DWD537", x=0, y=0, z=0, q=100
    ),
    dict(
        mac="e3:3a:13:b2:5f:56", id="DW8615", x=-1, y=-1, z=-1, q=100
    )
]


async def launcher(list_cb: list):
    await asyncio.gather(*list_cb)


def launch_cli_client(list_cb: list):
    asyncio.run(launcher(list_cb=list_cb))


class CMDOption(Enum):
    params_host = "host"
    params_port = "port"
    params_mode = "mode"
    param_time_before = "time_before"
    param_time_after = "time_after"


class CMDMode(Enum):
    pub_ping_test = "pub_ping_test"
    sub_ping_test = "sub_ping_test"
    pub_serial = "pub_serial"
    pub_update_net = "pub_update_net"
    pub_test_update_net = "pub_test_update_net"
    pub_raspi_gpio="pub_raspi_gpio"
    sub_db_save_net = "sub_db_save_net"
    sub_db_rel = "sub_db_rel"
    sub_db_unrel = "sub_db_unrel"
    sub_db_serial = "sub_db_serial"
    sub_db_unrel_serial = "sub_db_unrel_serial"
    sub_raspi_gpio = "sub_raspi_gpio"
    repeater_gpio_to_net="repeater_gpio_to_net"
    rilevamento_pacchetti = "rilevamento_pacchetti"


class CMDSerial(Enum):
    serial_opt_path = "serial_path"
    serial_opt_baudrate = "serial_baudrate"
    serial_opt_timeout = "serial_timeout"

def launch_serial(host, port, cb, *args, serial_opt: str = None, channel: str = "/db_unrel", **kwargs):
    """
    I parametri in ingresso sono necessari per gestire la seriale di acquisizione dati
    """
    serial_path = None
    baudrate = 115200
    timeout = 1
    for label in kwargs.keys():
        if label == CMDSerial.serial_opt_baudrate.value:
            baudrate = kwargs.get(label, baudrate)
        elif label == CMDSerial.serial_opt_path.value:
            serial_path = kwargs.get(label, serial_path)
        elif label == CMDSerial.serial_opt_timeout.value:
            timeout = int(kwargs.get(label, timeout))
    launch_cli_client([
        wrapper_serial_callback_pub(
            host=host, port=port,
            channel=channel,
            serial_path=serial_path,
            baudrate=baudrate,
            timeout=timeout,
            cb=cb,
            mark_ts=dt.utcnow().__str__(),
            id_send=serial_path,
            time_wait_before=float(kwargs.get(
                CMDOption.param_time_before.value)),
            time_wait_after=float(kwargs.get(
                CMDOption.param_time_after.value)),
        )
    ])


def launch_rilevamento_pacchetti(*args, port: int = None, host: str = None, **kwargs):
    """
    Utility per lanciare il sistema pronto per recuperare i dati durante il rilevamento a pacchetti
    """
    launch_cli_client([wrapper_callback_sub(
        host=host, port=port,
        channel=channel,
        cb=orm.cmd.save_net,
        db_ref="unrel",
        topic_response="/net/refresh",
        time_wait_before=float(kwargs.get(
            CMDOption.param_time_before.value)),
        time_wait_after=float(kwargs.get(
            CMDOption.param_time_after.value)),
        **params) for params, channel in [
            (dict(filter_mac_permitted=[
             "aa:aa:aa:aa", "ff:ff:ff:ff"]), "/net/update"),
            (dict(filter_mac_permitted=[
             "aa:aa:aa:aa", "ff:ff:ff:ff"]), "/geo/update"),
            (dict(log_data=True), "/net/archive")
    ]
    ])


def launch(*args, **kwargs):
    try:
        mode = kwargs[CMDOption.params_mode.value]
        kwargs[CMDOption.params_port.value] = int(
            kwargs[CMDOption.params_port.value])
        mode = [single for single in CMDMode if single.value == mode][0]
    except Exception as e:
        print("Errore nei parametri di ingresso", e)
        exit(1)

    try:
        host = kwargs[CMDOption.params_host.value]
        port = int(kwargs[CMDOption.params_port.value])
    except:
        print("PArametri di connessione al broker non completi", e)
        exit(1)
    if mode == CMDMode.pub_update_net:
        # Sottoscrive tutte le richieste di aggiornamento della rete e pubblica sul /net lo stato attuale della rete
        launch_cli_client([wrapper_callback_sub(
            port=port, host=host,
            channel="/net/refresh",
            cb=orm.cmd.read_net,
            db_ref="serial",
            topic_response="/net",
            time_wait_before=float(kwargs.get(
                CMDOption.param_time_before.value)),
            time_wait_after=float(kwargs.get(
                CMDOption.param_time_after.value))
        )
        ])
    elif mode == CMDMode.sub_db_save_net:
        launch_cli_client([wrapper_callback_sub(
            port=port, host=host,
            channel="/net/update",
            cb=orm.cmd.save_net,
            db_ref="serial",
            topic_response="/net/refresh",
            time_wait_before=float(kwargs.get(
                CMDOption.param_time_before.value)),
            time_wait_after=float(kwargs.get(
                CMDOption.param_time_after.value))
        )
        ])
    # Pubblicazione dati da porta seriale
    elif mode == CMDMode.pub_serial:
        launch_serial(
            *args, cb=pubs.cmd_serial.unitn_raw_parse_message, **kwargs)
    # Ricezione dati per caso "Rilevamento Pacchetti" utilizzato per rilevare i dati in contesto statico
    elif mode == CMDMode.rilevamento_pacchetti:
        launch_rilevamento_pacchetti(*args,  **kwargs)
    # Comunicazione con GPIO: ricezione comandi per GPIO
    elif mode == CMDMode.pub_raspi_gpio:
        launch_serial(
            *args, cb=pubs.cmd_serial.unitn_raw_detect_allarm, channel="/gpio/update", **kwargs)
    # Comunicazione con GPIO: richiesta accensione GPIO
    elif mode == CMDMode.sub_raspi_gpio:
        launch_cli_client([wrapper_callback_sub(port=port, host=host,
                                                channel="/gpio/update",
                                                cb=subs.cmd_gpio_raspi.set_gpio,
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value))
                                                )])
    elif mode == CMDMode.repeater_gpio_to_net:
        launch_cli_client([wrapper_callback_sub(port=port, host=host,
                                                channel="/gpio/update",
                                                cb=subs.cmd_simulation.echo,
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value)),
                                                topic_response="/net/update"
                                                )])
    # Utility Generiche
    # Salvataggio dati su database influxdb (time-serial)
    elif mode == CMDMode.sub_db_serial:
        launch_cli_client([wrapper_callback_sub(port=port, host=host,
                                                channel="/db_serial",
                                                cb=orm.cmd.query_serial, mark_ts=str(
                                                    dt.utcnow()),
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value))
                                                )])
    # salvataggio dati per mongodb o per porta seriale
    elif mode in [CMDMode.sub_db_unrel, CMDMode.sub_db_unrel_serial]:
        cb = orm.cmd.query_unrel
        if mode == CMDMode.sub_db_unrel_serial:
            cb = orm.cmd.save_serial_data
        launch_cli_client([
            wrapper_callback_sub(port=port, host=host,
                                 channel="/db_unrel",
                                 cb=cb,
                                 mark_ts=str(dt.utcnow(),
                                             time_wait_before=float(kwargs.get(
                                                 CMDOption.param_time_before.value)),
                                             time_wait_after=float(kwargs.get(
                                                 CMDOption.param_time_after.value)))),
        ])
    # Utility per Test
    elif mode == CMDMode.pub_test_update_net:
        launch_cli_client([wrapper_callback_pub(port=port, host=host,
                                                channel="/net/update",
                                                cb=pubs.cmd_simulation.movement, nodes=sample_nodes,
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value))
                                                )
                           ])
    elif mode == CMDMode.pub_ping_test:
        launch_cli_client([wrapper_callback_pub(port=port, host=host,
                                                channel="/ping", cb=ping, mark_ts=dt.utcnow().__str__(),
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value)))])
    elif mode == CMDMode.sub_ping_test:
        launch_cli_client([wrapper_callback_sub(port=port, host=host,
                                                channel="/ping", cb=ping, mark_ts=dt.utcnow().__str__(),
                                                time_wait_before=float(kwargs.get(
                                                    CMDOption.param_time_before.value)),
                                                time_wait_after=float(kwargs.get(
                                                    CMDOption.param_time_after.value)))])
    else:
        print("Opzione non prevista")
        exit(2)


def option():
    """
    Differneti opzioni per lanciare il proprio script
    """
    parser = argparse.ArgumentParser(add_help="Differenti Modalità di lancio")
    parser.add_argument(
        '-p', '--port',
        help="Porta di accesso al broker mqtt",
        dest=CMDOption.params_port.value,
        default="1883",
    )
    parser.add_argument(
        '-i', '--ip',
        help="Host di accesso al broker mqtt",
        dest=CMDOption.params_host.value,
        default="localhost"
    )
    parser.add_argument(
        '--mode',
        choices=[k.value for k in CMDMode],
        dest=CMDOption.params_mode.value,
        default="-missing-"
    )
    parser.add_argument(
        '-wb', '--wait_second_before',
        dest=CMDOption.param_time_before.value,
        default=0
    )
    parser.add_argument(
        '-wa', '--wait_second_after',
        dest=CMDOption.param_time_after.value,
        default=0.05
    )
    parser.add_argument(
        '-sb', '--serial_baudrate',
        dest=CMDSerial.serial_opt_baudrate.value,
        default=115200
    )
    parser.add_argument(
        '-sp', '--serial_path',
        dest=CMDSerial.serial_opt_path.value,
        default=None
    )
    parser.add_argument(
        '-st', '--serial_timeout',
        dest=CMDSerial.serial_opt_timeout.value,
        default=1
    )
    opt = parser.parse_args()
    return opt.__dict__


if __name__ == "__main__":
    opts = option()
    launch(**opts)
