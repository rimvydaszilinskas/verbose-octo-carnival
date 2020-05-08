FROM python:3

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code/
RUN pip install -r requirements.txt
RUN chmod +x /code/start.sh
