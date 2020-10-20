from types import SimpleNamespace

from orm.cfg import DB_PARAM

client = SimpleNamespace()
if DB_PARAM.get("dbseries", dict()).get("driver", "") == "influxdb":
    config = DB_PARAM["dbseries"]
    from .proxy_db import *
    for single_table in config["db_tables"]:
        setattr(client, single_table, DB(
            db_name=config["database"],
            db_table=single_table, host=config["host"], port=config["port"],
            username=config["username"], password=config["password"]
        ))
