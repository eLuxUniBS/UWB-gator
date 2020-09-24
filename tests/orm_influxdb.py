from datetime import datetime
from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'delete_me')

client.create_database('delete_me')
json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": datetime.utcnow(),
        "fields": {
            "value": 0.64
        }
    },
    {
        "measurement": "single_node",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time":"",
        "id_node": "DCA!",
        "fields": {
            "x": 0.64,
            "y": 0.64,
            "z": 0.64,
            "q": 0.64,
        }
    }
]

client.write_points([x for x in json_body if x["measurement"]=="single_node"])
client.write_points([x for x in json_body if x["measurement"]!="single_node"])
result = client.query('select value from cpu_load_short;')
print(result)
result = client.query('select value from single_node;')
print(result)