
from pymodm import MongoModel
from datetime import datetime as dt
from pymodm import MongoModel, fields

class RawSignal(MongoModel):
    """
    {'header': {'ts_send': datetime.datetime(2021, 5, 9, 15, 36, 1, 522412), 'task_id': '583e6a63-91ab-4227-aaaa-4bb851f85f99', 'task_name': 'app.service.tasks.core.dispatcher'},
    'routing_key': 'worker.db.save', 'exchange': 'exchangeUSBSerial',
    'body': {'detected': True, 'ts_collected': datetime.datetime(2021, 5, 9, 15, 36, 1, 522273),
    'raw_distance': '346', 'distance': '351', 'first_peak_pwr': '-82858', 'receive_power': '-80654',
    'frequency_offset': '6545',
    'raw_content': '17->d537: SUCCESS 346 bias 351 fppwr -82858 rxpwr -80654 cifo 6545\n', 'sender': '17', 'receiver': 'd537'}}
    """
    # Dati collezionati
    message_d_sender = fields.CharField(blank=True)  # ID
    message_d_receiver = fields.CharField(blank=True)  # ID
    message_d_raw_distance = fields.CharField(blank=True)
    message_d_distance = fields.CharField(blank=True)
    message_d_first_peak_pwr = fields.CharField(blank=True)
    message_d_receive_power = fields.CharField(blank=True)
    message_d_frequency_offset = fields.CharField(blank=True)
    # Tempistiche messaggio
    message_ts_collected = fields.DateTimeField(blank=True)  # Get from source
    message_ts_sendit = fields.DateTimeField(blank=True)  # Send by worker
    # Messaggio originale
    message_raw_content = fields.CharField(blank=True)  # A raw copy
    ts = fields.DateTimeField()
    id_sender = fields.CharField(blank=True)  # ID Sender

    @classmethod
    def create(cls, header: dict = None, body: dict = None):
        if header is None or body is None:
            return None
        base_datetime = dt(year=2000, month=1, day=1)
        obj = cls(            
            message_d_sender=body.get("sender", None),
            message_d_receiver=body.get("receiver", None),
            message_d_raw_distance=body.get("raw_distance", None),
            message_d_distance=body.get("distance", None),
            message_d_first_peak_pwr=body.get("first_peak_pwr", None),
            message_d_receive_power=body.get("receive_power", None),
            message_d_frequency_offset=body.get("frequency_offset", None),
            message_ts_collected=body.get("ts_collected", base_datetime),
            message_ts_sendit=header.get("ts_send", header.get("ts", base_datetime)),
            message_raw_content=body.get("raw_content", None),
            id_sender=header.get("id_send","-missing-"),
            ts=dt.utcnow()
        )
        obj.save()
        print("SAVED {}@{} ts_collected {} ts_sendit {}".format(cls.__name__,obj.ts,obj.message_ts_collected,obj.message_ts_sendit))


class GoodSignal(MongoModel):
    """
    {'header': {'ts_send': datetime.datetime(2021, 5, 9, 15, 36, 1, 522412), 'task_id': '583e6a63-91ab-4227-aaaa-4bb851f85f99', 'task_name': 'app.service.tasks.core.dispatcher'},
    'routing_key': 'worker.db.save', 'exchange': 'exchangeUSBSerial',
    'body': {'detected': True, 'ts_collected': datetime.datetime(2021, 5, 9, 15, 36, 1, 522273),
    'raw_distance': '346', 'distance': '351', 'first_peak_pwr': '-82858', 'receive_power': '-80654',
    'frequency_offset': '6545',
    'raw_content': '17->d537: SUCCESS 346 bias 351 fppwr -82858 rxpwr -80654 cifo 6545\n', 'sender': '17', 'receiver': 'd537'}}
    """
    # Dati collezionati
    message_d_sender = fields.CharField(blank=True)  # ID
    message_d_receiver = fields.CharField(blank=True)  # ID
    message_d_raw_distance = fields.CharField(blank=True)
    message_d_distance = fields.CharField(blank=True)
    message_d_first_peak_pwr = fields.CharField(blank=True)
    message_d_receive_power = fields.CharField(blank=True)
    message_d_frequency_offset = fields.CharField(blank=True)
    # Tempistiche messaggio
    message_ts_collected = fields.DateTimeField(blank=True)  # Get from source
    message_ts_sendit = fields.DateTimeField(blank=True)  # Send by worker
    # Messaggio originale
    message_raw_content = fields.CharField(blank=True)  # A raw copy
    ts = fields.DateTimeField()
    id_sender = fields.CharField(blank=True)  # ID Sender

    @classmethod
    def create(cls, header: dict = None, body: dict = None):
        if header is None or body is None:
            return None
        if body.get("detected", False) is False:
            return None
        base_datetime = dt(year=2000, month=1, day=1)
        obj = cls(
            message_d_sender=body.get("sender", None),
            message_d_receiver=body.get("receiver", None),
            message_d_raw_distance=body.get("raw_distance", None),
            message_d_distance=body.get("distance", None),
            message_d_first_peak_pwr=body.get("first_peak_pwr", None),
            message_d_receive_power=body.get("receive_power", None),
            message_d_frequency_offset=body.get("frequency_offset", None),
            message_ts_collected=body.get("ts_collected", base_datetime),
            message_ts_sendit=header.get("ts_send", header.get("ts", base_datetime)),
            message_raw_content=body.get("raw_content", None),
            id_sender=header.get("id_send","-missing-"),
            ts=dt.utcnow()
        )
        obj.save()
        print("SAVED GOOD {} {}".format(cls.__name__,obj.ts))
