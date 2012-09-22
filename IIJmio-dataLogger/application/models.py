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


# ファミリーなら3つのsim_service_code
class ServiceModel(db.Model):
    service_code = db.StringProperty(required=True)
    sim_service_code = db.StringProperty(required=True)


class SimInfoModel(db.Model):
    sim_service_code = db.StringProperty(required=True)
    phone_number = db.IntegerProperty(required=True)
    iccid = db.StringProperty(required=True)
    sim_type = db.StringProperty(required=True, indexed=False)
    status = db.StringProperty(required=True,  indexed=False)


class SimLogModel(db.Model):
    iccid = db.StringProperty(required=True)
    date = db.DateProperty(required=True)
    usage = db.IntegerProperty(required=True, indexed=False)
    updated_at = db.DateTimeProperty(auto_now=True, indexed=False)


class SimDetailLogModel(db.Model):
    iccid = db.StringProperty(required=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    remaining_coupons = db.IntegerProperty(required=True, indexed=False)


class ServiceDetailLogModel(db.Model):
    service_code = db.StringProperty(required=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    total_remaining_amount = db.IntegerProperty(required=True, indexed=False)
    remaining_coupons = db.IntegerProperty(required=True, indexed=False)
