# -*- coding: utf-8 -*-
"""
models.py

App Engine datastore models

"""
from google.appengine.ext import db


# ユーザーの情報
class UserModel(db.Model):
    mio_id = db.StringProperty(required=True)
    password = db.StringProperty(required=True, indexed=False)
    service_code = db.StringProperty(required=True, indexed=False)


# ファミリーなら3つのsim
class SimInfoModel(db.Model):
    service_code = db.StringProperty(required=True)
    sim_service_code = db.StringProperty(required=True)
    phone_number = db.StringProperty(required=True)
    iccid = db.StringProperty(required=True)
    sim_type = db.StringProperty(required=True, indexed=False)
    status = db.StringProperty(required=True,  indexed=False)


class SimLogModel(db.Model):
    iccid = db.StringProperty(required=True)
    usage = db.IntegerProperty(required=True, indexed=False)
#    created_at = db.DateProperty(indexed=False)
    updated_at = db.DateTimeProperty(auto_now=True)


class SimDetailLogModel(db.Model):
    iccid = db.StringProperty(required=True)
    remaining_coupons = db.IntegerProperty(required=True, indexed=False)
    updated_at = db.DateTimeProperty(auto_now=True)


class ServiceDetailLogModel(db.Model):
    service_code = db.StringProperty(required=True)
    total_remaining_amount = db.IntegerProperty(required=True, indexed=False)
    remaining_coupons = db.IntegerProperty(required=True, indexed=False)
    updated_at = db.DateTimeProperty(auto_now=True)
