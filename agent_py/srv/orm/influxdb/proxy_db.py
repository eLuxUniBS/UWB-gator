from influxdb import InfluxDBClient
from datetime import datetime as dt
import json,time,copy


class DB:
    def __init__(self, db_name=None, db_table=None, db_host="localhost",
                 db_port="8086", db_username="root", db_password="root",force_time:bool=False,remove_fields:list=[], **kwargs):
        self.db_name = db_name
        self.measurement_name = db_table
        self.port = int(db_port)
        self.host = db_host
        self.force_time=force_time
        self.remove_fields=remove_fields
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
            if content.get("time", None) is None or self.force_time:
                content["time"] = dt.utcnow().__str__()
            for field in self.remove_fields:
                if content["tags"].get(field,None) is not None:
                    del content["tags"][field]
                if content["fields"].get(field,None) is not None:
                    del content["fields"][field]       
            self.client.write_points(points=[content])
            return dict(response=200)
        except Exception as e:
            print("CREATE ERROR")
            print(e)
            return dict(response=500)

    def read(self, measurement=None):
        if measurement is None:
            measurement = self.measurement_name
        try:
            return dict(response=200, data=list(self.client.query(
                "select * from {}".format(measurement)).raw["series"]))
        except Exception as e:
            print("Read Query INFLUXDB ERROR\n", e)
            return dict(response=500)

    def write(self, measurement=None, **kwargs):
        if kwargs is None:
            return dict(response=500)
        if measurement is None:
            measurement = self.measurement_name
        return self.create(measurement=measurement, **kwargs)

    def query(self,content:dict, *args,**kwargs):
        """
        Formato messaggio: in kwargs viene passato il payload
        {
            "header": _client.clientID,
            "payload": {
            "query": "save",
                "data": {
                    "fields": {"mac": mac.toString(), "x": x, "y": y, "z": z, "q": q},
                    "tags": {"id": id, "ts": time}
                }
            }
        }
        """
        if content.get("query", None) is not None:
            if content.get("query").find("get") == 0:
                return self.read(**content.get("data", dict()))
            elif content.get("query").find("save") == 0:
                data=content.get("data", dict())
                resp=[]
                if type(data) == list:
                    for single_data in data:
                        temp=copy.deepcopy(single_data)
                        resp.append(self.write(**temp))
                else:                    
                    temp=copy.deepcopy(data)
                    resp.append(self.write(**temp))
                return resp
        return None
