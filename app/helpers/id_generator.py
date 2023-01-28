from app.database.db import CouponDbConnection


def referral_number_generator(type):
    """
    get last id by type and id keys for generate new record for other services.
    """
    try:
        with CouponDbConnection() as mongo:

            referral_number = mongo.counter_collection.find_one({"type": type})
            if referral_number is not None:
                mongo.counter_collection.update_one({"type": type}, {
                    "$set": {"referral_number": int(referral_number["referral_number"] + 1)}})
                return int(referral_number["referral_number"]) + 1
            else:
                mongo.counter_collection.insert_one({"type": type, "referral_number": 1})
                return 1
    except:
        return {"success": False, "message": "Dealership: شماره سفارش تولید نشد"}
