import time
from datetime import datetime

from source.helpers.connection import MongoConnection
from source.modules.date_convertor import jalali_datetime


class Coupon:
    def __init__(self, token: str = None, coupon_id: int = 0, coupon_name: str = None, prefix: str = ""):
        self.token = token
        self.coupon_name = coupon_name
        self.coupon_tokens: list = []
        self.coupon_id = coupon_id
        self.status: str = "pend"
        self.start_date: str = ""
        self.end_date: str = ""
        self.conditions: object = {}
        self.event: str = ""
        self.event_name: str = ""
        self.whole_sales_number: int = 0
        self.whole_sold_number: int = 0
        self.daily_sales_number: int = 0
        self.customer_sales_number: int = 0
        self.customer_sold_number: int = 0
        self.bought_customer_ids: list = []
        self.bought_customer_groups: list = []
        self.prefix: str = prefix

    def get_next_sequence_coupon_id(self):
        """
        auto increment id generator for self object
        :return: True if coupon is the first obj or correct id has been generated
        """
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                coupon_id = mongo.counter.find_one({"type": "coupon"}, projection_operator)
                if coupon_id is not None:
                    self.coupon_id = coupon_id.get("couponId") + 1
                    mongo.counter.update_one({"type": "coupon"}, {"$set": {"couponId": self.coupon_id}})
                    if coupon_id.get("couponId") < 1000:
                        mongo.counter.update_one({"type": "coupon"}, {"$set": {"couponId": 1000}})
                else:
                    mongo.counter.insert_one({"type": "coupon", "couponId": 1000})
                    self.coupon_id = 1000
                return True
            except Exception:
                return False

    def is_coupon_name_exists(self) -> bool:
        query_operator = {"couponName": self.coupon_name}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            return bool(mongo.coupon.find_one(query_operator, projection_operator))

    @staticmethod
    def is_prefix_exists(prefix: str) -> bool:
        query_operator = {"couponPrefix": prefix}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            return bool(mongo.coupon.find_one(query_operator, projection_operator))

    def is_coupon_exists(self) -> bool:
        query_operator = {"couponId": self.coupon_id}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            return bool(mongo.coupon.find_one(query_operator, projection_operator))

    def save(self,
             customer_sales_number,
             whole_sales_number,
             coupon_daily_sales_number,
             start_date,
             end_date,
             coupon_type,
             prefix,
             tokens_list
             ):
        if not self.get_next_sequence_coupon_id():
            return False
        coupon_data: dict = {
            "couponName": self.coupon_name,
            "couponId": self.coupon_id,
            "couponCreateTime": time.time(),
            "couponJalaliCreateTime": jalali_datetime(datetime.now()),
            "couponStatus": "pend",
            "couponCustomerSalesNumber": customer_sales_number,
            "couponDailySalesNumber": coupon_daily_sales_number,
            "couponWholeSoldNumber": 0,
            "couponWholeSalesNumber": whole_sales_number,
            "couponJalaliStartDate": start_date,
            "couponJalaliEndDate": end_date,
            "couponType": coupon_type,
            "couponPrefix": prefix or None,
            "couponConditions": {},
            "couponTokens": tokens_list
        }
        with MongoConnection() as mongo:
            result: object = mongo.coupon.insert_one(coupon_data)
            if result.acknowledged:
                return self.coupon_id
        return False

    def edit_coupon(self,
                    coupon_name=None,
                    customer_sales_number=None,
                    whole_sales_number=None,
                    start_date=None,
                    end_date=None,
                    coupon_daily_sales_number=None
                    ):
        query_operator = {"couponId": self.coupon_id}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            coupon = mongo.coupon.find_one(query_operator, projection_operator)
            modify_operator = {
                "$set": {
                    "couponName": coupon_name or coupon.get("couponName"),
                    "couponCustomerSalesNumber": customer_sales_number or coupon.get("couponCustomerSalesNumber"),
                    "couponDailySalesNumber": coupon_daily_sales_number or coupon.get("couponDailySalesNumber"),
                    "couponWholeSalesNumber": whole_sales_number or coupon.get("couponWholeSalesNumber"),
                    "couponJalaliStartDate": start_date or coupon.get("couponJalaliStartDate"),
                    "couponJalaliEndDate": end_date or coupon.get("couponJalaliEndDate"),
                }
            }
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator,
            ):
                return bool(result.acknowledged)
        return

    def get_next_auto_priority(self) -> int:
        query_operator = {"couponId": self.coupon_id}
        projection_operator = {"_id": 0, "couponConditions": 1}
        with MongoConnection() as mongo:
            try:
                result = mongo.coupon.find_one(
                    query_operator, projection_operator
                )
                priority = 0
                for condition, value in result.get("couponConditions").items():
                    if value.get("priority") > priority:
                        priority = value.get("priority")
                return priority + 1
            except Exception:
                return 1

    def set_condition(self, condition_type: str, data: dict) -> bool:
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$set": {
                f"couponConditions.{condition_type}": data
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator,
            ):
                return bool(result.acknowledged)
        return False

    def get_coupon(self):
        query_operator = {"couponId": self.coupon_id}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                return mongo.coupon.find_one(query_operator, projection_operator)
            except Exception:
                return False

    def delete(self):
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$set": {
                "couponStatus": "archive",
                "couponJalaliDeleteTime": jalali_datetime(datetime.now()),
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator,
            ):
                return bool(result.acknowledged)
        return

    def activate(self):
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$set": {
                "couponStatus": "active",
                "couponJalaliActivateTime": jalali_datetime(datetime.now()),
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator,
            ):
                return bool(result.acknowledged)
        return

    def deactivate(self):
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$set": {
                "couponStatus": "pend"
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator
            ):
                return bool(result.acknowledged)
        return

    def get_coupon_by_prefix(self):
        query_operator = {"couponPrefix": self.prefix}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if result := mongo.coupon.find_one(query_operator, projection_operator):
                    self.coupon_id = result.get("couponId")
                    return result
                return False
            except Exception:
                return False

    def check_coupon_is_valid(self):
        query_operator = {"couponPrefix": self.prefix}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if result := mongo.coupon.find_one(query_operator, projection_operator):
                    return (result.get("couponWholeSoldNumber") < result.get("couponWholeSalesNumber") and result.get(
                        "couponJalaliStartDate") <= jalali_datetime(datetime.now()) <= result.get(
                        "couponJalaliEndDate") and result.get("couponStatus") == "active"), result
            except Exception:
                return False, False

    def check_public_token(self, token: str, customer_id: int):
        query_operator = {"prefix": self.prefix}
        projection_operator = {"_id": 0}
        with MongoConnection() as mongo:
            try:
                if result := mongo.coupon.find_one(query_operator, projection_operator):
                    ...
            except Exception:
                return False

    def check_coupon_for_private_customer(self, token: str, customer_id: int, max_use: int):
        with MongoConnection() as mongo:
            return list(mongo.coupon.aggregate([
                {
                    "$match":
                        {
                            "couponId": self.coupon_id,
                            "couponTokens": {
                                "$and": [{
                                    "$elemMatch":
                                        {
                                            "token": token,
                                            "used": {"$lt": max_use}
                                        }
                                },
                                    {
                                        "customerId": customer_id
                                    }
                                ]
                            }
                        }
                }
            ]))

    def check_coupon_for_public_customer(self, token: str, customer_id: int, max_use):
        with MongoConnection() as mongo:
            result = list(mongo.coupon.aggregate([
                {
                    "$match":
                        {
                            "couponId": self.coupon_id,
                            "couponTokens": {
                                "$elemMatch":
                                    {
                                        # "token": token,
                                        "customerId": customer_id,
                                        "used": {"$gte": max_use}
                                    }
                            }
                        }
                }
            ]))
            return not len(result)

    def check_token(self, token: str):
        with MongoConnection() as mongo:
            return list(mongo.coupon.aggregate([
                {
                    "$match":
                        {
                            "couponId": self.coupon_id,
                            "couponTokens": {
                                "$elemMatch":
                                    {
                                        "token": token
                                    }
                            }
                        }
                }
            ]))

    def get_all_conditions(self):
        with MongoConnection() as mongo:
            return mongo.coupon.find_one(
                {"couponId": self.coupon_id},
                {"couponConditions": 1, "_id": 0}).get("couponConditions") or False

    def get_coupon_type(self):
        query_operator = {"couponId": self.coupon_id}
        with MongoConnection() as mongo:
            if result := mongo.coupon.find_one(
                    query_operator,
                    {"_id": 0, "couponType": 1},
            ):
                return result.get("couponType")
            return False

    def use_public_coupon(self, coupon_id, customer_id, token, order_number):
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$inc": {
                "couponWholeSoldNumber": 1,
            },
            "$set": {
                "couponStatus": "archive",
                "couponJalaliUseTime": jalali_datetime(datetime.now()),
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    {"couponId": self.coupon_id, "couponTokens.token": token, "couponTokens.customerId": customer_id},
                    {"$inc": {"couponWholeSoldNumber": 1, "couponTokens.$.used" : 1}},
                    # {"$arrayFilters": [{"couponTokens.token": token, "customerId": customer_id}, {"$upsert": False}]}
            ):
                return result.modified_count

    def use_private_coupon(self, coupon_id, customer_id, token, order_number):
        query_operator = {"couponId": self.coupon_id}
        modify_operator = {
            "$inc": {
                "couponWholeSoldNumber": 1,
            },
            "$set": {
                "couponStatus": "archive",
                "couponJalaliUseTime": jalali_datetime(datetime.now()),
            }
        }
        with MongoConnection() as mongo:
            if result := mongo.coupon.update_one(
                    query_operator,
                    modify_operator,
            ):
                return
