from abc import ABC, abstractmethod


class BackendPort(ABC):

    @abstractmethod
    def receive_schedules(self):
        pass


class FeederJobPort(ABC):

    @abstractmethod
    def serve_portion(self, feeder_id: int):
        pass
