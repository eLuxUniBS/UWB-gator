DB_PARAM = {
    "db": {"driver": "mongo",
           "db_name": "test_secutor_home",
           "db_host": "localhost",
           "db_port": "20127"
           },
    "dbseries": {
        "driver": "influxdb",
        "host": '192.168.1.83',
        "port": "8086",
        "username": "root",
        "password": "root",
        "database": "test_secutor_home",
        "db_tables":["last","log"]
    }
}
