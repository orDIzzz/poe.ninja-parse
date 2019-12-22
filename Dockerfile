FROM ubuntu:latest
MAINTAINER ordizzz
RUN apt-get update && apt-get install python3.7 python3-pip build-essential python3-lxml firefox -y
RUN python3.7 -V
COPY . /PoE.Ninja.Parser
WORKDIR /PoE.Ninja.Parser
RUN chmod +x geckodriver && cp geckodriver /app/.heroku/python/bin
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
CMD python3 main.py
