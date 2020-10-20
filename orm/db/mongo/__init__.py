from orm.cfg import DB_PARAM

if DB_PARAM.get("db", dict()).get("driver", "") == "mongo":
    from pymodm import connect

    connect("mongodb://{user}:{password}@{host}:{port}/{db}".format
            (user=DB_PARAM["db"]["db_username"],
             password=DB_PARAM["db"]["db_password"],
             host=DB_PARAM["db"]["db_host"],
             port=DB_PARAM["db"]["db_port"],
             db=DB_PARAM["db"]["db_name"])
            )
    from .net import *
    from .user import *
    from .fleet import *
    from .permission import *