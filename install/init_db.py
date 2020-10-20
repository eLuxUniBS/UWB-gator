from orm import db
import json
import orm

input_data = dict()

with open("dataset.json", "rb") as target:
    input_data = json.load(target)


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
            print("ERRORE IN ",single)
            print(e)
            print("ERRORE")

def create_net():
    for single in input_data.get(orm.db.Node.__name__,[]):
        print(single)

if __name__ == "__main__":
    drop_database()
    create_net()
