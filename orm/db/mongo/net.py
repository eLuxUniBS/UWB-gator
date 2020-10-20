
from pymodm import MongoModel, fields


class Node(MongoModel):
    name = fields.CharField()
    macaddress = fields.CharField()
    cfg = fields.DictField()

    def to_dict(self):
        return dict(name=self.name,maccaddres=self.macaddress,cfg=self.cfg)

class SubNet(MongoModel):
    name = fields.CharField()
    node_assigned = fields.ListField()


class Net(MongoModel):
    """
    Con questa classe posso "immaginare" di segnare chi abbia "aperto" le chiavi
    """
    name = fields.CharField()
    cfg = fields.DictField()
    avaiable = fields.BooleanField(default=True)
    subnet = fields.EmbeddedDocumentListField(SubNet)
