
from pymodm import MongoModel, fields


class Node(MongoModel):
    name = fields.CharField()
    macaddress = fields.CharField()
    cfg = fields.DictField()


class SubNet(MongoModel):
    name = fields.CharField()
    node_assigned = fields.ReferenceField(Node,
                                          on_delete=fields.ReferenceField.DO_NOTHING)


class Net(MongoModel):
    """
    Con questa classe posso "immaginare" di segnare chi abbia "aperto" le chiavi
    """
    name = fields.CharField()
    cfg = fields.DictField()
    avaiable = fields.BooleanField(default=True)
    subnet = fields.ReferenceField(SubNet,
                                   on_delete=fields.ReferenceField.DO_NOTHING)
