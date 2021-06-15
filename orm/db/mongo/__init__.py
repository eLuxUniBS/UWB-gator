from orm.cfg import DB_PARAM

if DB_PARAM.get("db", dict()).get("driver", "") == "mongo":
    from pymodm import connect
    config=DB_PARAM["db"]
    user_credentials=""
    if config.get("db_username",None) is not None and config.get("db_password",None) is not None:
            user_credentials="{user}:{password}@".format(user=config["db_username"],
             password=config["db_password"])
    try:
        connect("mongodb://{user_credentials}{host}:{port}/{db}{append_option_query}".format
                (user_credentials=user_credentials,
                 host=config["db_host"],
                 port=config["db_port"],
                 db=config["db_name"],
                append_option_query=config["option_query"])
                )
    except Exception as e:
        print("Attenzione, errore in recupero connessione a DB")
        print(e)
    from .net import *
    from .user import *
    from .fleet import *
    from .permission import *
    from .signal import *