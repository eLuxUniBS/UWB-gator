from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import MongoModel, fields

from .base_model import BaseModel

class LogOpening(BaseModel):
    """
    Con questa classe posso "immaginare" di segnare chi abbia "aperto" le chiavi
    """
    header = fields.DictField()
    when = fields.DateTimeField()
    body = fields.DictField()


class UserPatents(BaseModel):
    user = fields.ReferenceField("User",
                                 on_delete=fields.ReferenceField.DO_NOTHING)
    vehicle = fields.ReferenceField("Vehicle",
                                    on_delete=fields.ReferenceField.DO_NOTHING)
