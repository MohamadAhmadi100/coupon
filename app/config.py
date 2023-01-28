import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")

    COUPON_MONGO_HOST: str = os.getenv("COUPON_MONGO_HOST")
    COUPON_MONGO_PORT: int = int(os.getenv("COUPON_MONGO_PORT"))
    COUPON_MONGO_USER: str = os.getenv("COUPON_MONGO_USER")
    COUPON_MONGO_PASS: str = os.getenv("COUPON_MONGO_PASS")

    RABBIT_HOST: str = os.getenv("RABBIT_HOST")
    RABBIT_PORT: int = int(os.getenv("RABBIT_PORT"))
    RABBIT_USER: str = os.getenv("RABBIT_USER")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS")

settings = Settings()
