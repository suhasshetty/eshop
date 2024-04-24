from django.db import models
from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from enum import Enum

from phonenumber_field.modelfields import PhoneNumberField
from simple_history import register


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    UNDISCLOSED = "Undisclosed"

    @classmethod
    def choices(obj):
        return tuple((item.value, item.name) for item in obj)

class User(AbstractUser):
    display_name = CharField(max_length=64)
    date_of_birth = DateField(default=timezone.now)
    gender = CharField(max_length=16, choices=Gender.choices())
    phone_number = PhoneNumberField()
    address = TextField(null=True, blank=True)


# class Address(Model):
#     address = CharField(max_length=512)
#     city = CharField(max_length=64)
#     state = CharField(max_length=64)
#     country = CharField(max_length=64)
#     zip_code = CharField(max_length=16)
#     addressee = ManyToManyField(User, on_delete=DO_NOTHING)


# class Seller(User):
#     taxation_id = CharField(max_length=32)
#     brand_name = CharField(max_length=64)
#     business_email = models.EmailField(blank=True, null=True)
#     business_phone_number = PhoneNumberField(blank=True, null=True)
#     business_address = ForeignKey(Address, on_delete=DO_NOTHING, blank=True, null=True)


register(User)
