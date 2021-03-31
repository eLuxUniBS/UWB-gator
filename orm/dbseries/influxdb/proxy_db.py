from influxdb import InfluxDBClient
from datetime import datetime as dt


class DB:
    def __init__(self, db_name=None, db_table=None, db_host="localhost",
                 db_port="8086", db_username="root", db_password="root",**kwargs):
        self.db_name = db_name
        self.measurement_name = db_table
        self.port = int(db_port)
        self.host = db_host
        self.client = InfluxDBClient(host=self.host, port=self.port, username=db_username,
                                     password=db_password, database=self.db_name)

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
            return dict(response=200, data=list(self.client.query(
                "select * from {}".format(measurement)).raw["series"]))
        except Exception as e:
            print("Read Query INFLUXDB ERROR\n",e)
            return dict(response=500)


    def write(self, measurement=None,**kwargs):
        if kwargs is None:
            return dict(response=500)
        if measurement is None:
            measurement=self.measurement_name
        return self.create(measurement=measurement,**kwargs)

    def query(self,*args,**kwargs):
        if len(args)==1:
            content=args[0]
        else:
            print(args)
            return dict(response=500)
        if content.get("query",None) is not None:
            if content.get("query").find("get")==0:
                return self.read(**content.get("data",dict()))
            elif content.get("query").find("save")==0:
                return self.write(**content.get("data",dict()))
        return None