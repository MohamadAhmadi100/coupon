from source.models.coupon import Coupon
from source.modules.cart_checker import CheckCart


def get_sorted_conditions(coupon):
    conditions = coupon.get_all_conditions()
    return {condition: conditions.get(condition) for condition in
            sorted(conditions, key=lambda condition: (conditions[condition]["priority"]), reverse=True)}


result = {}


def check_conditions(customer_id: int, cart: dict, coupon, coupon_data):
    conditions = get_sorted_conditions(coupon)
    if not conditions:
        return {"success": False, "error": "کد وارد شده قابل استفاده نیست", "status_code": 404}
    for condition, data in conditions.items():
        check_cart = CheckCart(customer_id, cart, coupon_data)
        exec(f"global result; result = check_cart.{condition}()")
        if result:
            return {"success": True, "message": result.get("message"), "coupon": result.get("coupon"),
                    "data": result.get("data"), "status_code": 200}
    return {"success": False, "error": "کد مورد نظر برای شما قابل استفاده نیست", "status_code": 404}


def check_coupon_type(customer_id: int, token: str, cart: dict, coupon, coupon_data):
    if coupon_data.get("couponType") == "private":
        result = coupon.check_coupon_for_private_customer(token=token, customer_id=customer_id,
                                                          max_use=coupon_data.get("couponCustomerSalesNumber") or 2)
        if not result:
            return {"success": False, "error": "این کد متعلق به شخص دیگری است", "status_code": 404}
    else:
        result = coupon.check_coupon_for_public_customer(token=token, customer_id=customer_id,
                                                         max_use=coupon_data.get("couponCustomerSalesNumber") or 2)
        if not result:
            return {"success": False, "error": "تعداد استفاده از این کد به حد نصاب رسیده است", "status_code": 404}
    return check_conditions(customer_id=customer_id, cart=cart, coupon=coupon, coupon_data=coupon_data)


def get_token(customer_id: int, token: str, cart: dict, coupon):
    if not coupon.get_coupon_by_prefix():
        return {"success": False, "error": "کد مورد نظر موجود نیست", "status_code": 404}
    if not coupon.check_token(token=token):
        return {"success": False, "error": "کد وارد شده اشتباه است", "status_code": 404}
    check_coupon_valid, coupon_data = coupon.check_coupon_is_valid()
    return check_coupon_type(customer_id, token, cart, coupon, coupon_data) if check_coupon_valid else {
        "success": False, "error": "زمان استفاده از این کد به پایان رسیده است", "status_code": 422}


def check_coupon(customer_id: int, token: str, cart: dict):
    if type(token) != str or "-" not in token:
        return {"success": False, "error": "کد وارد شده اشتباه است", "status_code": 404}
    prefix = token.split("-")[0].upper()
    coupon = Coupon(prefix=prefix)
    return get_token(customer_id, token, cart, coupon)


def use_coupon(customer_id, coupon_id, token, order_number):
    coupon = Coupon(coupon_id=coupon_id)
    coupon.use_coupon(coupon_id, customer_id, token, order_number)

# coupon = Coupon(prefix="ananas", coupon_id=1006)
# print(check_coupon(customer_id=12, token="STRING-BEA5", cart={"dd": "dff"}))
