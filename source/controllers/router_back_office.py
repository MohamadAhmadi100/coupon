import json

from source.models.coupon import Coupon
from source.modules import log
from source.modules.token_generator import Token
from source.modules.setter import Filter
from source.modules.getter import GetData


def create_coupon(coupon_name: str, customer_sales_number: int, whole_sales_number: int, start_date: str, end_date: str,
                  coupon_daily_sales_number: int, coupon_type: str, prefix: str = None, staff_user_id: int = 20000):
    coupon = Coupon(coupon_name=coupon_name)
    if coupon.is_coupon_name_exists():
        return {"success": False, "error": "نام کد تخفیف تکراری است", "status_code": 422}
    if coupon.is_prefix_exists(prefix=prefix.upper()):
        return {"success": False, "error": "پیشوند کد تخفیف تکراری است", "status_code": 422}
    if coupon_type == "private":
        tokens_list: str = Token().private_tokens_list_generator(prefix, whole_sales_number)
    else:
        tokens_list: str = Token().public_tokens_list_generator(prefix, whole_sales_number)
    if coupon_id := coupon.save(customer_sales_number=customer_sales_number, whole_sales_number=whole_sales_number,
                                coupon_daily_sales_number=coupon_daily_sales_number, start_date=start_date,
                                end_date=end_date, coupon_type=coupon_type, prefix=prefix.upper(),
                                tokens_list=tokens_list):
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


def set_and_edit_condition(coupon_id: int, condition_type: str, data: dict, staff_user_id: int, priority: int = 0):
    coupon = Coupon(coupon_id=coupon_id)
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف وجود ندارد", "status_code": 404}
    if not priority:
        priority = coupon.get_next_auto_priority()
    # if coupon.get_coupon().get("couponType") == "private" and condition_type != "customer":
    #     return {"success": False, "error": "برای کدهای اختصاصی فقط شرط مشتری خاص فعال است", "status_code": 422}
    if coupon.set_condition(condition_type=condition_type, data=dict(data, **{"priority": priority})):
        log.save_condition_log(coupon_id=coupon_id, staff_id=staff_user_id)
        return {"success": True, "message": "شرط با موفقیت ثبت شد", "data": {"couponId": coupon_id},
                "status_code": 200}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 417}


def get_all_available_coupons_crm(data: str = None):
    try:
        data = {} if data is None else json.loads(data)
        records = Filter()
        period_filters: dict = {}
        value_filters: dict = {}
        search_query: dict = {}
        if filters := data.get("filters"):
            period_filters: dict = records.set_period_filters(filters) or {}
            value_filters: dict = records.set_value_filters(filters) or {}
        if search_phrase := data.get("search"):
            search_query = records.set_search_query(search_phrase)
        filters = dict(period_filters, **value_filters, **search_query)
        if not data.get("sortType"):
            sort_type = "asc"
        else:
            sort_type = "asc" if data.get("sortType") == "ascend" else "desc"
        sort_name = data.get("sortName") or "couponId"
        return GetData().executor(
            queries=filters,
            number_of_records=data.get("perPage") or "15",
            page=data.get("page") or "1",
            sort_name=sort_name,
            sort_type=sort_type or "asc"
        )
    except Exception as e:
        return {"success": False, "error": e, "status_code": 404}


def get_coupon_by_id(coupon_id: int):
    coupon = Coupon(coupon_id=coupon_id)
    if coupon.is_coupon_exists():
        return {"success": True, "message": coupon.get_coupon(), "status_code": 200}
    return {"success": False, "error": "کد تخفیف مورد نظر موجود نیست ", "status_code": 404}


def delete_coupon(coupon_id: int, staff_user_id: int = 20000):
    coupon = Coupon(coupon_id=coupon_id)
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف مورد نظر موجود نیست", "status_code": 404}
    if coupon.delete():
        return {"success": True, "message": "کد تخفیف با موفقیت حذف شد", "status_code": 200}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 422}


def activate_coupon(coupon_id: int, staff_user_id: int = 20000):
    coupon = Coupon(coupon_id=coupon_id)
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف مورد نظر موجود نیست", "status_code": 404}
    if coupon.activate():
        return {"success": True, "message": "کد تخفیف با موفقیت فعال شد", "status_code": 200}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 422}


def deactivate_coupon(coupon_id: int, staff_user_id: int = 20000):
    coupon = Coupon(coupon_id=coupon_id)
    if not coupon.is_coupon_exists():
        return {"success": False, "error": "کد تخفیف مورد نظر موجود نیست", "status_code": 404}
    if coupon.deactivate():
        return {"success": True, "message": "کد تخفیف با موفقیت غیر فعال شد", "status_code": 200}
    return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 422}


def use_coupon(coupon_id: int, customer_id: int, token: str, order_number: int):
    coupon = Coupon(coupon_id=coupon_id)
    coupon_type = coupon.get_coupon_type()
    if coupon_type == "public":
        return coupon.use_public_coupon(coupon_id, customer_id, token, order_number)
    else:
        result = coupon.use_private_coupon()
    # if coupon.deactivate():
    # return {"success": True, "message": "کد تخفیف با موفقیت ثبت شد", "status_code": 200}
    # return {"success": False, "error": "مشکلی رخ داد. لطفا مجددا تلاش کنید", "status_code": 422}


# print(use_coupon(1008, 100, "STRING-BEA5", 5666))
