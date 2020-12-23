FROM python:3.8-slim

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app
WORKDIR /app
ENV CONFIG_PATH=config.yaml
ENV SETTINGS=Default
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python -m hub
