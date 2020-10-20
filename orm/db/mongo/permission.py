from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import MongoModel, fields


class LogOpening(MongoModel):
    """
    Con questa classe posso "immaginare" di segnare chi abbia "aperto" le chiavi
    """
    header = fields.DictField()
    when = fields.DateTimeField()
    body = fields.DictField()

    class Meta:
        indexes =[IndexModel([('key_signed', TEXT)])]


class UserPatents(MongoModel):
    user = fields.ReferenceField("User",
                                 on_delete=fields.ReferenceField.DO_NOTHING)
    vehicle = fields.ReferenceField("Vehicle",
                                    on_delete=fields.ReferenceField.DO_NOTHING)
