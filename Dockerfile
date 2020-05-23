FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update -q
RUN apt-get install -yq netcat
COPY . /code/