from mongoengine import *

class WifiNetwork(Document):
    ssid = StringField(required=True)
    password = StringField(required=True)

class Users(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    active = BooleanField(default=False)

class Device(Document):
    owner = ReferenceField(Users)

    meta = {'allow_inheritance': True}

class LED(Device):
    power_on = BooleanField(default=False)
    brightness = IntField(default=0, min_value=0, max_value=255)
