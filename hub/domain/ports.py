from abc import ABC, abstractmethod


class FeederCommunicationPort(ABC):

    @abstractmethod
    def receive_schedules(self):
        pass
