FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh