from hub.adapters.led_feeder_job_adapter import LedFeederJob
import os
import sys

from hub.adapters.google_adapter import GoogleSubAdapter
from hub.adapters.lora_adapter import LoraFeederJob
from hub.domain.ports import BackendPort, FeederJobPort


class Settings(object):
    backend: BackendPort = None
    feeder_job: FeederJobPort = None


class GoogleSettings(Settings):
    backend = GoogleSubAdapter
    feeder_job = LoraFeederJob

class LedSettings(Settings):
    backend = GoogleSubAdapter
    feeder_job = LedFeederJob


class DefaultSettings(Settings):
    backend = GoogleSubAdapter
    feeder_job = LoraFeederJob


def get_settings() -> Settings:
    cls_prefix = str.capitalize(os.environ.get("SETTINGS", "Default"))
    cls_name = f"{cls_prefix}Settings"
    return getattr(sys.modules[__name__], cls_name)
