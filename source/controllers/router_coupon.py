from source.models.coupon import Coupon


def check_coupon(customer_id: int, token: str, cart: dict):
    if type(token) != str or "-" not in token:
        return {"success": False, "error": "کد وارد شده اشتباه است", "status_code": 404}
    prefix = token.split("-")[0].upper()
    coupon = Coupon(prefix=prefix)
    # if not coupon.get_coupon_by_prefix():
    #     return {"success": False, "error": "کد مورد نظر موجود نیست", "status_code": 404}
    check_coupon_valid, coupon_data = coupon.check_coupon_is_valid()
    # if not check_coupon_valid:
    #     return {"success": False, "error": "زمان استفاده از این کد به پایان رسیده است", "status_code": 422}
    coupon.coupon_id = coupon_data.get("couponId")
    # if coupon_data.get("couponType") == "private":
    #     result = coupon.check_coupon_for_private_customer(token=token, customer_id=customer_id,
    #                                                       max_use=coupon_data.get("couponCustomerSalesNumber") or 2)
    #     if not result:
    #         return {"success": False, "error": "این کد متعلق به شخص دیگری است", "status_code": 404}
    #     result = coupon.check_coupon_for_public_customer(token=token, customer_id=customer_id,
    #                                                      max_use=coupon_data.get("couponCustomerSalesNumber") or 2)
    #     if not result:
    #         return {"success": False, "error": "تعداد استفاده از این کد به حد نصاب رسیده است", "status_code": 404}
    # if not coupon.check_token(token=token):
    #     return {"success": False, "error": "کد وارد شده اشتباه است", "status_code": 404}
    # if check_token is None:
    #     return {"success": False, "error": "کد وارد شده اشتباه است", "status_code": 404}
    # elif result.get("couponType") == "private" and check_token is False:
    #     return {"success": False, "error": "کد وارد شده متعلق به شخص دیگری است", "status_code": 404}

    return {"success": True, "message": "مبلغ 322000 تومان از سبد شما کسر شد",
            "data": dict(cart, **{"coupon": coupon_data}), "status_code": 200}

# coupon = Coupon(prefix="ananas", coupon_id=1006)
# print(coupon.check_coupon_for_private_customer(token="ANANAS-34538B", customer_id=123, max_use=2))
