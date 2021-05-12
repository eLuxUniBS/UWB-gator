DB_PARAM = {
    "db": {"driver": "mongo",
           "db_name": "test_rilevamento_statico",
           "db_host": "localhost",
           "db_port": "17017",
           "db_username": "root",
           "db_password": "root",
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
## Local DEV
# DB_PARAM = {
#     "db": {"driver": "mongo",
#            "db_name": "test_secutor_home",
#            "db_host": "localhost",
#            "db_port": "29127"
#            },
#     "dbseries": {
#         "driver": "influxdb",
#         "host": 'localhost',
#         "port": "8086",
#         "username": "root",
#         "password": "root",
#         "database": "test_secutor_home",
#         "db_tables":["last","log"]
#     }
# }
# DB_PARAM = {
#     "db": {"driver": "mongo",
#            "db_name": "test_secutor_home",
#            "db_host": "localhost",
#            "db_port": ""
#            },
#     "dbseries": {
#         "driver": "influxdb",
#         "host": 'localhost',
#         "port": "28127",
#         "token":"IJD9EtstUEQgUQgluW0I4LkwLpQLh0n5EP02zIerYS98_Q0EA4trRX_TBxDx1pt7heusiQ6TgDjX3EAaPMQXww==",
#         "database": "eseb",
#         "db_tables":["last","log"]
#     }
# }
