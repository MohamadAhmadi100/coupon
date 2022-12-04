import random
import string


class Token:
    def __init__(self):
        self.token: str = ""
        self.token_length: int = 8

    def generator(self) -> str:
        self.token: str = "".join(random.choice(string.hexdigits.upper()) for _ in range(self.token_length))
        return self.token

    def tokens_list_generator(self, token_quantity):
        return [self.generator() for _ in range(token_quantity)]
