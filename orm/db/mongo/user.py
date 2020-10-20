from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel, EmbeddedMongoModel


class User(MongoModel):
    matricola = fields.CharField()
    avaiable = fields.BooleanField(default=True)

    class Meta:
        indexes = [IndexModel([('matricola', TEXT)])]


class Profile(MongoModel):
    email = fields.EmailField()
    user = fields.ReferenceField(User,
                                 on_delete=fields.ReferenceField.DO_NOTHING)
    nome = fields.CharField()
    secondo_nome = fields.CharField()
    cognome = fields.CharField()


class ClientKeyPair(MongoModel):
    """
    Accoppiamento chiavi
    """
    user = fields.ReferenceField(User,
                                 on_delete=fields.ReferenceField.DO_NOTHING)
    key_signed = fields.CharField()
    key_added = fields.DateTimeField()
    key_opened = fields.ReferenceField("LogOpening",
                                       on_delete=fields.ReferenceField.DO_NOTHING)

    class Meta:
        indexes = [IndexModel([('key_signed', TEXT)]),
                   IndexModel([('key_added', TEXT)])]


class EquipmentUser(MongoModel):
    key_signed = fields.ReferenceField(ClientKeyPair,
                                       on_delete=fields.ReferenceField.DO_NOTHING)
    assigned_from = fields.DateTimeField()
    assigned_until = fields.DateTimeField()
    configuration = fields.DictField()
