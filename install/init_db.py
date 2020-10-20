import json
from time import time
from datetime import datetime as dt
from bson import ObjectId
from agent.position import format_message_position
import orm

input_data_json = dict()
input_data_csv = list()


def read_keys_by_line(line: str = None):
    if line is None:
        return dict()
    buffer = dict()
    for key in line.split(","):
        buffer[key.strip()] = None
    return buffer


def prepare_dataset(file_json=None, file_csv=None):
    global input_data_json, input_data_csv
    if file_json is not None:
        with open(file_json, "rb") as target:
            input_data_json = json.load(target)
    content = []
    if file_csv is not None:
        with open(file_csv, "rb") as target:
            content = target.readlines()
    scheme = dict()
    for raw_line in content:
        line = raw_line.decode("utf-8")
        if line[0].strip() == "#":
            scheme = read_keys_by_line(line[1:])
            continue
        buffer_scheme = scheme.copy()
        data = line.split(",")
        for index in range(0, len(data)):
            buffer_scheme[list(buffer_scheme.keys())[index]] = data[
                index].strip()
        input_data_csv.append(buffer_scheme)


def drop_database():
    for single in [
        orm.db.Net,
        orm.db.SubNet,
        orm.db.Node,
        # User
        orm.db.User,
        orm.db.Profile,
        orm.db.ClientKeyPair, orm.db.EquipmentUser,
        # Fleet
        orm.db.Vehicle,
        orm.db.VehicleKeyPair,
        orm.db.EquipmentVehicle,
        # Permission
        orm.db.LogOpening,
        orm.db.UserPatents]:
        try:
            single.objects.all().delete()
        except Exception as e:
            print("ERRORE IN ", single)
            print(e)
            print("ERRORE")


def create_net():
    for super_node in input_data_csv:
        node = orm.db.Node(
            name=super_node["nodeName"],
            macaddress=super_node["macAddr"],
            cfg=dict(
                name_dev=super_node["nameHW"],
                type_dev=super_node["typeDev"],
                node_type=super_node["nodeType"],
                node_symbol=super_node["nodeSymbol"],
                node_role=super_node["nodeRole"],
            )).save()
        subnets = list(orm.db.SubNet.objects.raw({"name": super_node["cell"]}))
        subnet = None
        try:
            net = orm.db.Net.objects.get(
                dict(
                    name=super_node["net"]
                )
            )
            for list_subnet in subnets:
                if list_subnet in net.subnet:
                    subnet = list_subnet
                    break
        except Exception:
            net = orm.db.Net(name=super_node["net"], avaiable=True).save()
        if subnet is None:
            subnet = orm.db.SubNet(name=super_node["cell"]).save()
            net.subnet.append(subnet)
            net.save()
        if node.pk not in subnet.node_assigned:
            subnet.node_assigned.append(node.pk.__str__())
            subnet.save()


if __name__ == "__main__":
    # DB SERIES
    orm.dbseries.client.last.drop_db()
    orm.dbseries.client.last.create_db()
    # DB
    prepare_dataset(file_csv="dataset.csv")
    drop_database()

    create_net()
    collect_node = dict()
    for net in orm.db.Net.objects.raw(dict(avaiable=True)):
        collect_node[net.name] = dict()
        for subnet in net.subnet:
            collect_node[net.name][subnet.name] = dict()
            obj_subnet = orm.db.SubNet.objects.get(dict(_id=subnet.pk))
            for node_id in obj_subnet.node_assigned:
                node = orm.db.Node.objects.get(
                    dict(_id=ObjectId(node_id)))
                collect_node[net.name][subnet.name][node.pk.__str__()] \
                    = node.to_dict()
                orm.dbseries.client.last.create(**format_message_position(
                    id_name=node.cfg["name_dev"],
                    mac_address=node.macaddress,
                    val_time=0))
                orm.dbseries.client.log.create(**format_message_position(
                    id_name=node.cfg["name_dev"],
                    mac_address=node.macaddress,
                    ts_send=dt.utcnow().timestamp() * 1e6))
