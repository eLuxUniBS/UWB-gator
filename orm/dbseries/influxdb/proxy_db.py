from influxdb import InfluxDBClient
from datetime import datetime as dt


class DB:
    def __init__(self, db_name=None, db_table=None, host="localhost",
                 port="8086", username="root", password="root"):
        self.db_name = db_name
        self.measurement_name = db_table
        self.port = int(port)
        self.host = host
        self.client = InfluxDBClient(host=host, port=port, username=username,
                                     password=password, database=db_name)

    def drop_db(self):
        self.client.drop_database(self.db_name)

    def create_db(self):
        self.client.create_database(self.db_name)

    def create(self, measurement=None, **dataset):
        try:
            content = dict(
                measurement=measurement if measurement is not None else self.measurement_name,
                **dataset
            )
            print(content)
            if content.get("time", None) is None:
                content["time"] = dt.utcnow()
            self.client.write_points([content])
            return dict(response=200)
        except Exception as e:
            print(e)
            return dict(response=500)

    def read(self, measurement=None):
        if measurement is None:
            measurement=self.measurement_name
        try:
            return dict(response=200, data=self.client.query(
                "select * from {}".format(measurement)).raw)
        except Exception as e:
            print(e)
            return dict(response=500)
