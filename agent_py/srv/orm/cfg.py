import os
# Parametri standard per una connessione ai servizi in locale (utili per il testing)
DB_PARAM = {
    "db": {"driver": "mongo",
           "db_name": "test_rilevamento_statico_locale",
           "db_host": "localhost",
           "db_port": "20127",
           "option_query": "?authSource=admin"
           },
    "dbseries": {
        "driver": "influxdb",
        "db_host": 'localhost',
        "db_port": "8086",
        "db_username": "root",
        "db_password": "root",
        "db_database": "test_rilevamento_statico_locale",
        "db_tables": {"log": {"force_time": True}, "last": {"remove_fields": ["ts"]}}
    }
}
# PArametri di configurazione pensati per l'uso su container docker
if os.environ.get("DOCKER_ENV", None) is not None:
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
            "db_tables": {"log": {"force_time": True}, "last": {"remove_fields": ["ts"]}}
        }
    }
