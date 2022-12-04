import json

from source.models.coupon import Coupon
from source.modules import log


def create_coupon(coupon_name: str, customer_sales_number: int, whole_sales_number: int, start_date: str, end_date: str,
                  coupon_daily_sales_number: int, coupon_type: str, prefix: str = None, staff_user_id: int = 20000):
    coupon = Coupon(coupon_name=coupon_name)
    if coupon.is_coupon_name_exists():
        return {"success": False, "error": "نام کد تخفیف تکراری است", "status_code": 422}
    if coupon_id := coupon.save(customer_sales_number=customer_sales_number, whole_sales_number=whole_sales_number,
                                coupon_daily_sales_number=coupon_daily_sales_number, start_date=start_date,
                                end_date=end_date, coupon_type=coupon_type, prefix=prefix):
        log.save_create_log(coupon_id=coupon_name, staff_id=staff_user_id)
        return {"success": True, "message": "کد تخفیف با موفقیت ایجاد شد", "data": {"couponId": coupon_id},
                "status_code": 201}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 417}


def edit_coupon(data: str, staff_user_id: int = 20000):
    data = json.loads(data)
    coupon = Coupon(coupon_id=data.get("coupon_id"))
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف وجود ندارد", "status_code": 404}
    if _result := coupon.edit_coupon(data.get("coupon_name"), data.get("customer_sales_number"),
                                     data.get("whole_sales_number"), data.get("start_date"), data.get("end_date"),
                                     data.get("coupon_daily_sales_number")):
        log.save_edit_log(coupon_id=data.get("coupon_id"), staff_id=staff_user_id)
        return {"success": True, "message": "کد تخفیف با موفقیت ویرایش شد", "data": {"couponId": data.get("coupon_id")},
                "status_code": 201}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 417}


def set_and_edit_condition(coupon_id: int, condition_type: str, data: dict, staff_user_id: int, priority: int = 1):
    coupon = Coupon(coupon_id=coupon_id)
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف وجود ندارد", "status_code": 404}
    if coupon.set_condition(condition_type=condition_type, data=dict(data, **{"priority": priority})):
        log.save_condition_log(coupon_id=coupon_id, staff_id=staff_user_id)
        return {"success": True, "message": "شرط با موفقیت ثبت شد", "data": {"couponId": coupon_id},
                "status_code": 201}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 417}
