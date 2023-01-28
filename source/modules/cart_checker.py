class CartInitialize:
    def __init__(self, cart):
        self.products: list = cart.get("products", [])
        self.baskets: object = cart.get("baskets", {})
        self.cart_user_id: int = cart.get("userInfo").get("userId")

    def get_price(self):
        return sum(product.get("price") * product.get("count") for product in self.products)


class CheckCart:
    def __init__(self, customer_id: int, cart: dict, coupon_data):
        self.customer_id = customer_id
        self.cart = cart
        self.coupon_data = coupon_data

    def category(self, data):
        return False

    def basketSum(self):
        condition = self.coupon_data.get("couponConditions").get("basketSum")
        cart = CartInitialize(cart=self.cart)
        cart_price = cart.get_price()
        if cart_price >= condition.get("minBasketSum"):
            discount = condition.get("discount").get("value") or condition.get("discount").get(
                "percentage") * cart_price
            final_price = cart_price - discount
            coupon = {
                "couponName": self.coupon_data.get("couponName"),
                "couponId": self.coupon_data.get("couponId"),
                "condition": condition,
                "couponCartPrice": final_price,
                "discountValue": discount
            }
            return {"message": f"مبلغ {discount} تومان تخفیف به شما تعلق گرفت ",
                    "data": {"couponPrice": final_price, "discount": discount}, "coupon": coupon}
        return False

    def product(self):
        return {"message": "dssddsd"}

    def customerGroup(self):
        return {"message": "dssddsd"}

    def customer(self):
        return {"message": "dssddsd"}

    def event(self):
        return {"message": "dssddsd"}

    def minProductQuantity(self):
        return {"message": "dssddsd"}
