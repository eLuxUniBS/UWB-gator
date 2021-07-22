from bson import ObjectId
from pymodm import MongoModel, fields

from agent_py.srv.orm.mongo.base_model import BaseModel


class Node(BaseModel):
    name = fields.CharField()
    macaddress = fields.CharField()
    cfg = fields.DictField()

    def to_dict(self):
        return dict(name=self.name,maccaddres=self.macaddress,cfg=self.cfg)

    @classmethod
    def get_by_id(cls,id):
        return cls.objects.get(dict(_id=ObjectId(id)))

class SubNet(BaseModel):
    name = fields.CharField()
    node_assigned = fields.ListField()

    @classmethod
    def get_by_id(cls,id):
        return cls.objects.get(dict(_id=ObjectId(id)))

class Net(BaseModel):
    """
    Con questa classe posso "immaginare" di segnare chi abbia "aperto" le chiavi
    """
    name = fields.CharField()
    cfg = fields.DictField()
    avaiable = fields.BooleanField(default=True)
    subnet = fields.EmbeddedDocumentListField(SubNet)
