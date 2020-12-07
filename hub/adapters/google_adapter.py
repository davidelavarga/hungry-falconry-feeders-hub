import logging
import os

from google.api_core.exceptions import AlreadyExists
from google.protobuf.duration_pb2 import Duration

from hub.domain.ports import FeederCommunicationPort
from google.cloud import pubsub_v1  # TODO Use Pub/Sub Lite instead Pub/Sub

from utils.get_config import get_config
from utils.mac import get_mac

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# PROJECT_ID = pubsub_config.get("project_id")


class GooglePubSubAdapter(FeederCommunicationPort):

    def __init__(self):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = get_or_create_subscription()

    @staticmethod
    def callback(message):
        print("Received message: {}".format(message))
        message.ack()

    def receive_schedules(self):
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=self.callback)
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with self.subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                # streaming_pull_future.result(timeout=timeout)
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
            "message_retention_duration": Duration(seconds=get_config().get("message_retention_duration", 7126560)),
            "ack_deadline_seconds": get_config().get("ack_deadline_seconds", 300),
            "filter": f'attributes.mac = "{get_mac()}"'
        })
        logging.info(f"{sub_path} created")
    except AlreadyExists:
        logging.info(f"{sub_path} already exists")
        return sub_path

    return sub_path


def get_subs_name(subs_type: str):
    mac = get_mac()
    return f"{mac}-{subs_type}"


sub = get_or_create_subscription()
print(sub)
