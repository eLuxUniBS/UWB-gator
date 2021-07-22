from types import SimpleNamespace

from srv.orm.cfg import DB_PARAM

client = SimpleNamespace()
if DB_PARAM.get("dbseries", dict()).get("driver", "") == "influxdb":
    config = DB_PARAM["dbseries"]
    from srv.orm.influxdb.proxy_db import *

    for single_table in config["db_tables"].keys():
        params = dict(
            db_name=config["db_database"],
            db_table=single_table, db_host=config["db_host"], db_port=config["db_port"])
        if config.get("token", None) is None:
            params["db_username"] = config["db_username"]
            params["db_password"] = config["db_password"]
        else:
            params["db_token"] = config["db_token"]
        setattr(client, single_table, DB(**{**params,**config["db_tables"][single_table]}))
