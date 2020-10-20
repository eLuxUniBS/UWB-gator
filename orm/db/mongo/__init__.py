from orm.cfg import DB_PARAM

if DB_PARAM.get("db", dict()).get("driver", "") == "mongo":
    from pymodm import connect
    config=DB_PARAM["db"]
    connect("mongodb://{user}:{password}@{host}:{port}/{db}".format
            (user=config["db_username"],
             password=config["db_password"],
             host=config["db_host"],
             port=config["db_port"],
             db=config["db_name"])
            )
    from .net import *
    from .user import *
    from .fleet import *
    from .permission import *