FROM ubuntu:latest
MAINTAINER ordizzz
RUN apt-get update && apt-get install python3 python3-pip build-essential gunicorn -y
RUN python3 -V
COPY . /PoE.Ninja.Parser
WORKDIR /PoE.Ninja.Parser
ENV LANG=C.UTF-8
ENV LC_CTYPE="C.UTF-8"
ENV LC_NUMERIC="C.UTF-8"
ENV LC_TIME="C.UTF-8"
ENV LC_COLLATE="C.UTF-8"
ENV LC_MONETARY="C.UTF-8"
ENV LC_MESSAGES="C.UTF-8"
ENV LC_PAPER="C.UTF-8"
ENV LC_NAME="C.UTF-8"
ENV LC_ADDRESS="C.UTF-8"
ENV LC_TELEPHONE="C.UTF-8"
ENV LC_MEASUREMENT="C.UTF-8"
ENV LC_IDENTIFICATION="C.UTF-8"
ENV LC_ALL=C.UTF-8
RUN pip3 install -r requirements.txt --upgrade
EXPOSE 8000
CMD python3 main.py
