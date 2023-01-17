import random
import string


class Token:
    def __init__(self):
        self.token: str = ""
        self.token_length: int = 4

    def generator(self, prefix) -> str:
        self.token: str = f"{prefix.upper()}-" + "".join(
            random.choice(string.hexdigits.upper()) for _ in range(self.token_length))
        return self.token

    def private_tokens_list_generator(self, prefix, token_quantity):
        return [{"token": self.generator(prefix), "used": 0, "customerId": 0, "cartId": 0} for _ in
                range(token_quantity)]

    def public_tokens_list_generator(self, prefix, token_quantity):
        public_token = self.generator(prefix)
        return [{"token": public_token, "used": 0, "customerId": 0, "cartId": 0} for _ in
                range(token_quantity)]
