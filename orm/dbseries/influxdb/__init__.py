from types import SimpleNamespace

from orm.cfg import DB_PARAM

client = SimpleNamespace()
if DB_PARAM.get("dbseries", dict()).get("driver", "") == "influxdb":
    config = DB_PARAM["dbseries"]
    from .proxy_db import *

    for single_table in config["db_tables"]:
        params = dict(
            db_name=config["database"],
            db_table=single_table, host=config["host"], port=config["port"])
        if config.get("token", None) is None:
            params["username"] = config["username"]
            params["password"] = config["password"]
        else:
            params["token"] = config["token"]
        setattr(client, single_table, DB(**params))
