"""
connection to mongo db
"""

from pymongo import MongoClient

from app.config import settings

class CouponDbConnection:
    def __init__(self):
        self.connection = MongoClient(
            settings.COUPON_MONGO_HOST, int(settings.COUPON_MONGO_PORT), username=settings.COUPON_MONGO_USER,
            password=settings.COUPON_MONGO_PASS)
        # self.database = self.connection["supplier"]
        # self.supplier_collection = self.database["supplier"]
        self.databaseCoupon = self.connection["coupon"]
        self.coupon = self.databaseCoupon["coupon"]
        self.counter_collection = self.databaseCoupon["id_generator"]
        # self.databaseTransfer = self.connection["transfer"]
        # self.transfer_collection = self.databaseTransfer["transfer"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
