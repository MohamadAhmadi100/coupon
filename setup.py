import os

from setuptools import setup

requirements_dir = os.getcwd() + "/requirements.txt"
with open(requirements_dir, "r") as f:
    file = f.readlines()
    requirements = [line.rstrip() for line in file]

setup(
    name=" coupon",
    version="0.1.0",
    packages=["app"],
    url="",
    license="",
    author="Fatemeh Sabzevari",
    author_email="",
    install_requires=requirements,
    description="",
)
