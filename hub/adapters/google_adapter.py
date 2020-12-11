import json
import logging
from typing import Callable

from google.api_core.exceptions import AlreadyExists
from google.protobuf.duration_pb2 import Duration

from hub.domain.ports import BackendPort
from google.cloud import pubsub_v1  # TODO Use Pub/Sub Lite instead Pub/Sub

from hub.domain.schedule_builder import ScheduleBuilder
from utils.get_config import get_config
from utils.mac import get_mac


class GoogleSubAdapter(BackendPort):

    def __init__(self, job_scheduler: ScheduleBuilder, serve_job: Callable):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = get_or_create_subscription()
        self.job_scheduler = job_scheduler
        self.serve_job = serve_job

    def __callback(self, message):
        logging.info(f"Received message: {message}")
        self.job_scheduler.feeder_schedule_as_job(json.loads(message.data), self.serve_job)
        message.ack()

    def receive_schedules(self):
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=self.__callback)
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        logging.info(f"Getting msgs from {self.subscription_path} ...")
        with self.subscriber:
            try:
                return streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()


def get_or_create_subscription():
    conf = get_config()["google_pub_sub"]
    project_id, topic_id = conf["project_id"], conf["topic_id"]
    subscription_id = get_subs_name(conf["subscription"].get("type", "schedule-consumer"))

    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    sub_path = subscriber.subscription_path(project_id, subscription_id)
    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        subscriber.create_subscription(request={
            "name": sub_path,
            "topic": topic_path,
            "message_retention_duration": Duration(
                seconds=conf["subscription"].get("message_retention_duration", 86400)),
            "ack_deadline_seconds": conf["subscription"].get("ack_deadline_seconds", 300),
            "filter": f'attributes.mac = "{get_mac()}"'
        })
        logging.info(f"{sub_path} created")
    except AlreadyExists:
        logging.info(f"{sub_path} already exists")
        return sub_path

    return sub_path


def get_subs_name(subs_type: str):
    mac = get_mac()
    return f"{subs_type}-{mac}"
