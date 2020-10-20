DB_PARAM = {
    "db": {"driver": "mongo",
           "db_username": "worker",
           "db_password": "worker_12345!",
           "db_name": "test_secutor",
           "db_host": "localhost",
           "db_port": "20127"
           },
    "dbseries": {
        "driver": "influxdb",
        "host": 'localhost',
        "port": "8086",
        "username": "root",
        "password": "root",
        "database": "test_secutor_series",
        "db_tables":["last","log"]
    }
}
