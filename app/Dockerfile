FROM python:3.10
WORKDIR /usr/app
RUN apt-get update --assume-yes
RUN apt-get install unixodbc-dev --assume-yes
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt