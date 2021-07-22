from bson import ObjectId
from pymodm import MongoModel


class BaseModel(MongoModel):

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(dict(_id=ObjectId(id)))
