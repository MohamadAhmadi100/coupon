import time
from datetime import datetime

from source.helpers.connection import MongoConnection
from source.modules.date_convertor import jalali_datetime


def save_create_log(coupon_id: str, staff_id: int = 20000) -> bool:
    pipeline = {
        "couponId": coupon_id,
        "staffId": staff_id,
        "action": "createCoupon",
        "customerActionTime": time.time(),
        "customerJalaliActionTime": jalali_datetime(datetime.now()),
        "actions": []
    }
    with MongoConnection() as mongo:
        result = mongo.log.insert_one(pipeline)
    return bool(result.acknowledged)


def save_edit_log(coupon_id: int, staff_id: int = 20000) -> bool:
    query_operator = {"couponId": coupon_id}
    pipeline = {
        "addToSet": {"actions": {
            "staffId": staff_id,
            "action": "editCoupon",
            "customerActionTime": time.time(),
            "customerJalaliActionTime": jalali_datetime(datetime.now())
        }}
    }
    with MongoConnection() as mongo:
        result = mongo.log.update_one(query_operator, pipeline, upsert=True)
    return bool(result.acknowledged)


def save_condition_log(coupon_id: int, staff_id: int = 20000) -> bool:
    query_operator = {"couponId": coupon_id}
    pipeline = {
        "$addToSet": {"actions": {
            "staffId": staff_id,
            "action": "setCouponCondition",
            "customerActionTime": time.time(),
            "customerJalaliActionTime": jalali_datetime(datetime.now())
        }}
    }
    with MongoConnection() as mongo:
        result = mongo.log.update_one(query_operator, pipeline, upsert=True)
    return bool(result.acknowledged)
