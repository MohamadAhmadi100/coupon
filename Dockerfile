FROM python:3.9

WORKDIR /coupon

COPY ./README.md /coupon/README.md

COPY ./requirements.txt /coupon/requirements.txt

COPY ./.env /coupon/.env

COPY ./app/config.py /coupon/config.py

COPY ./setup.py /coupon/setup.py

COPY ./app /coupon/app

RUN pip install -e /coupon/.

CMD ["python", "/coupon/app/main.py"]
