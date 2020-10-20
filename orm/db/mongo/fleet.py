from pymodm import MongoModel, fields
from pymongo import IndexModel, TEXT


class Vehicle(MongoModel):
    vehicle_name = fields.CharField()
    vehicle_class = fields.CharField()


class VehicleKeyPair(MongoModel):
    """
    Accoppiamento chiavi
    """
    vehicle = fields.ReferenceField(Vehicle)
    key_signed = fields.CharField()
    key_added = fields.DateTimeField()
    key_opened = fields.ReferenceField("LogOpening",
                                       on_delete=fields.ReferenceField.DO_NOTHING)

    class Meta:
        indexes = [IndexModel([('key_signed', TEXT)]),
                   IndexModel([('key_opened', TEXT)])]


class EquipmentVehicle(MongoModel):
    key_signed = fields.ListField()
    assigned_from = fields.DateTimeField()
    assigned_until = fields.DateTimeField()
    configuration = fields.DictField()
