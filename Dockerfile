FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update

COPY . /code/
RUN pip install -r requirements.txt
RUN chmod +x /code/start.sh
RUN chmod +x /code/start_pipe.sh
