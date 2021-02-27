FROM python:3.8-slim

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

WORKDIR /tmp
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN rm -rf /tmp

WORKDIR /app
COPY hub hub
RUN mkdir /app/credentials/
ENV CONFIG_PATH=config.yaml
ENV SETTINGS=Default

CMD python -mO hub
