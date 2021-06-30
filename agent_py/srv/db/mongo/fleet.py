from pymodm import fields
from pymongo import IndexModel,HASHED

from .base_model import BaseModel

class Vehicle(BaseModel):
    vehicle_name = fields.CharField()
    vehicle_class = fields.CharField()


class VehicleKeyPair(BaseModel):
    """
    Accoppiamento chiavi
    """
    vehicle = fields.ReferenceField(Vehicle)
    key_signed = fields.CharField()
    key_added = fields.DateTimeField()
    key_opened = fields.ReferenceField("LogOpening",
                                       on_delete=fields.ReferenceField.DO_NOTHING)

    class Meta:
        indexes = [IndexModel([('key_signed', HASHED)]),
                   IndexModel([('key_opened', HASHED)])]


class EquipmentVehicle(BaseModel):
    key_signed = fields.ListField()
    assigned_from = fields.DateTimeField()
    assigned_until = fields.DateTimeField()
    configuration = fields.DictField()
