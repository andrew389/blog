FROM python:3.12

WORKDIR /code

RUN apt update && apt -qy upgrade

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

WORKDIR /code/tg_bot