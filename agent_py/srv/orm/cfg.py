import os
DB_PARAM = {
    "db": {"driver": "mongo",
           "db_name": "test_rilevamento_statico",
           "db_host": "localhost",
        #    "db_port": "17017",
           "db_port": "27017",
        #    "db_username": "root",
        #    "db_password": "root",
           "option_query": "?authSource=admin"
           },
    "dbseries": {
        "driver": "influxdb",
        "db_host": 'localhost',
        "db_port": "18086",
        "db_username": "root",
        "db_password": "root",
        "db_database": "test_rilevamento_statico",
        "db_tables": ["last", "log"]
    }
}
if os.environ.get("DOCKER_ENV",None) is not None:
    DB_PARAM = {
        "db": {"driver": "mongo",
               "db_name": "test_rilevamento_statico",
               "db_host": "db_not_ser",
               "db_port": "27017",
               "db_username": "root",
               "db_password": "root",
               "option_query": "?authSource=admin"
               },
        "dbseries": {
            "driver": "influxdb",
            "db_host": 'db_ser',
            "db_port": "8086",
            "db_username": "root",
            "db_password": "root",
            "db_database": "test_rilevamento_statico",
            "db_tables": ["last", "log"]
        }
    }