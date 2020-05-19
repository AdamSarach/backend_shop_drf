FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD . /music_service/

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]