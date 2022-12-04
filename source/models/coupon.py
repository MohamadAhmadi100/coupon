import time
from datetime import datetime

from source.helpers.connection import MongoConnection
from source.modules.date_convertor import jalali_datetime


class Coupon:
    def __init__(self, coupon_main_code: str = None, coupon_id: int = 0, coupon_name: str = None):
        self.coupon_main_code = coupon_main_code
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
        self.daily_sold_number: int = 0
        self.customer_sales_number: int = 0
        self.customer_sold_number: int = 0
        self.bought_customer_ids: list = []
        self.bought_customer_groups: list = []
        self.prefix: str = ""

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
             prefix
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
            "couponDailySoldNumber": 0,
            "couponDailySalesNumber": coupon_daily_sales_number,
            "couponWholeSoldNumber": 0,
            "couponWholeSalesNumber": whole_sales_number,
            "couponJalaliStartDate": start_date,
            "couponJalaliEndDate": end_date,
            "couponType": coupon_type,
            "couponPrefix": prefix or None,
            "couponConditions": {}
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
            coupon = mongo.basket.find_one(query_operator, projection_operator)
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
