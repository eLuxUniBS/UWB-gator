from orm.cfg import DB_PARAM

if DB_PARAM.get("db", dict()).get("driver", "") == "mongo":
    from pymodm import connect
    config=DB_PARAM["db"]
    user_credentials=""
    if config.get("db_username",None) is not None and config.get("db_password",None) is not None:
            user_credentials="{user}:{password}@".format(user=config["db_username"],
             password=config["db_password"])
    connect("mongodb://{user_credentials}{host}:{port}/{db}".format
            (user_credentials=user_credentials,
             host=config["db_host"],
             port=config["db_port"],
             db=config["db_name"])
            )
    from .net import *
    from .user import *
    from .fleet import *
    from .permission import *