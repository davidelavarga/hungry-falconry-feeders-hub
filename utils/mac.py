from getmac import get_mac_address

from hub.exceptions import MACAddressNoConfigured


def get_mac() -> str:
    mac = str(get_mac_address())
    mac = mac.replace(":", "-")
    if not mac:
        raise MACAddressNoConfigured()
    return mac
