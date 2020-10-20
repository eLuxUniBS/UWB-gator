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

    def create_db(self):
        self.client.create_database(self.db_name)

    def create(self, measurement=None, **dataset):
        try:
            content = dict(
                measurement=measurement if measurement is not None else self.measurement_name,
                time=dt.utcnow(),
                **dataset

            )
            self.client.write_points([content])
            return dict(response=200)
        except Exception as e:
            print(e)
            return dict(response=500)

    def read(self, measurement=None):
        if measurement is None:
            return dict(response=400)
        try:
            return dict(response=200, data=self.client.query(
                "select * from {}".format(measurement)).raw)
        except Exception as e:
            print(e)
            return dict(response=500)
