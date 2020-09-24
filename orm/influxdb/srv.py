from datetime import datetime
from influxdb import InfluxDBClient


class DB:
    def __init__(self, db_name, db_table, host="localhost", port=8086):
        self.db_name = db_name
        self.measur_name = db_table
        self.port = port
        self.host = host
        self.client = InfluxDBClient(host=host, port=port, username='root', password='root', database=db_name)

    def create_db(self):
        self.client.create_database(self.db_name)

    def query(self, *args, **kwargs):
        query = [x for x in args if "query" in list(x.keys())]
        if len(query) <= 0:
            return dict(error="no data")
        cmd_label = query[0]["query"]
        cmd_value = query[0]["data"]
        if cmd_label.strip().lower() == "save":
            return self.save(**cmd_value)
        elif cmd_label.strip().lower() == "get":
            return self.retrieve(**cmd_value)
        return dict(error="no command")

    def save(self, measurement=None, **dataset):
        try:
            content = dict(
                measurement=measurement if measurement is not None else self.measur_name,
                time=datetime.utcnow(),
                **dataset

            )
            self.client.write_points([content])
            if content["measurement"] == self.measur_name:
                self.client.write_points([dict(
                    measurement="positions_register",
                    time="2000-01-01 00:00:00",
                    tags=dict(id=content["tags"]["id"],mac=content["fields"]["mac"]),
                    fields=dict(x=content["fields"]["x"], y=content["fields"]["y"], z=content["fields"]["z"],
                                q=content["fields"]["q"])
                )])
            return dict(response=200)
        except Exception as e:
            print(e)
            return dict(response=500)

    def retrieve(self, **dataset):
        if dataset.get("measurement", None) is None:
            return dict(response=400)
        try:
            return dict(response=200, data=self.client.query("select * from {}".format(dataset.get("measurement"))).raw)
        except Exception as e:
            print(e)
            return dict(response=500)
