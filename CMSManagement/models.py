from django.db import models as db
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from datetime import datetime


# Create your models here.

class UserInfo(AbstractUser):
    zh_name = db.CharField(max_length=20, blank=False, unique=True)
    phone = db.CharField(max_length=11, default='', unique=True, blank=False)
    detail = db.CharField(max_length=100, default='front_user')

    class Meta:
        verbose_name = 'UserInfo'
        # fields = '__all__'

    def __str__(self):
        return self.username


class authToken(db.Model):
    key = db.CharField(max_length=100, unique=True, blank=False, primary_key=True)
    create = db.DateTimeField(default=datetime.now(), blank=False)
    user_id = db.IntegerField(unique=True, blank=False)

    def __str__(self):
        return self.user_id


class PhoneManage(db.Model):
    os_type = (
        ('android', 'android'),
        ('ios', "ios")
    )

    home = (
        ("借出", 1),
        ("在库", 0)
    )

    dName = db.CharField(max_length=100, blank=False, unique=True)
    os_version = db.CharField(max_length=20, blank=False, unique=True)
    type = db.CharField(max_length=10, choices=os_type, verbose_name="device Type")
    imei = db.CharField(max_length=50, blank=False, unique=True)
    is_home = db.IntegerField(choices=home, blank=False)
    remarks = db.CharField(max_length=100)
    create_time = db.DateTimeField(default=datetime.now)
    out_time = db.DateTimeField(max_length=50)

    user_id = db.CharField(max_length=100)

    def __str__(self):
        return self.dName
