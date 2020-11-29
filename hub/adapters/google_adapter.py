import os

from hub.domain.ports import FeederCommunicationPort
from google.cloud import pubsub_v1  # TODO Use Pub/Sub Lite instead Pub/Sub

from utils.get_config import get_config
from utils.mac import get_mac

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# PROJECT_ID = pubsub_config.get("project_id")


class GooglePubSubAdapter(FeederCommunicationPort):

    def __init__(self):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path("PROJECT_ID", "SUBSCRIPTION_ID")

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
    # TODO test this
    subscriber = pubsub_v1.SubscriberClient()
    conf = get_config("config.yaml")["google_pub_sub"]
    project_id, topic_id = conf["project_id"], conf["topic_id"]
    subscription_id = get_subs_name(conf["subscription"].get("type", "schedule-consumer"))
    sub_path = subscriber.subscription_path(project_id, subscription_id)
    topic_path = subscriber.topic_path(project_id, topic_id)
    subscriber.create_subscription(request={"name": sub_path, "topic": topic_path})


def get_subs_name(subs_type: str):
    mac = get_mac()
    return f"{mac}-{subs_type}"
