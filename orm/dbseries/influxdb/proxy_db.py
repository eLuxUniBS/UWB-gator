from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime as dt


class DB:
    def __init__(self, token, db_name=None, db_table=None, host="localhost",
                 port="8086"):
        self.db_name = db_name
        self.measurement_name = db_table
        self.port = int(port)
        self.host = host
        self.client = InfluxDBClient(url="http://{host}:{port}".format(host=host, port=port), token=token)
        self.client_write_sync = self.client.write_api(write_options=SYNCHRONOUS)

    @property
    def org(self):
        return self.db_name

    @property
    def bucket(self):
        return self.db_name

    def drop_db(self):
        # TODO update
        self.client.delete_api().delete(0, dt.utcnow(), "time>=0", self.bucket, self.org)
        # self.client.delete_database(self.db_name)

    def create_db(self):
        # TODO update
        pass
        # self.client.create_database(self.db_name)

    def create(self, measurement=None, **dataset):
        try:
            content = dict(
                measurement=measurement if measurement is not None else self.measurement_name,
                **dataset
            )
            if content.get("time", None) is None:
                content["time"] = dt.utcnow()
            tags_list = []
            field_list = []
            for sublist in [[x, content["tags"][x]] for x in content["tags"].keys()]:
                for single in sublist:
                    tags_list.append(single)
            for sublist in [[x, content["fields"][x]] for x in content["fields"].keys()]:
                for single in sublist:
                    field_list.append(single)
            point = Point(content["measurement"])
            for tag_k in content["tags"].keys():
                point.tag(tag_k, content["tags"][tag_k])
            for field_k in content["fields"].keys():
                point.field(field_k, content["fields"][field_k])
            point.time(content["time"])
            # self.client.write_api()
            self.client_write_sync.write(self.bucket, self.org, point)
            return dict(response=200)
        except Exception as e:
            print(e)
            return dict(response=500)

    def read(self, measurement=None):
        if measurement is None:
            measurement = self.measurement_name
        try:
            return dict(response=200, data=self.client.query(
                "select * from {}".format(measurement)).raw)
        except Exception as e:
            print(e)
            return dict(response=500)

    def query(self, query, data: dict = None, *args, **kwargs):
        if query.find("get")==0:
            return dict(response=200,data=self.client.g)
        else:
            print("QUERY", query, "\nData", data, "\nargs", args, "\nKWARGS", kwargs)
