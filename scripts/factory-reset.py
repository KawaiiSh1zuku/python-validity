from validitysensor.sensor import factory_reset, RebootException
from validitysensor.usb import usb


def _reset_device():
    """USB-bus-level reset so the chip leaves any leftover TLS/secure session
    and comes back in plaintext mode. Required when the service was killed
    (e.g. SIGKILL or a crash) mid-init, leaving the device in secure mode."""
    import time
    import usb.core as ucore

    dev = ucore.find(idVendor=0x06cb, idProduct=0x00a2)
    if dev is None:
        print('06cb:00a2 not found on the USB bus')
        return
    try:
        dev.reset()
        print('USB device reset issued; waiting for re-enumeration...')
    except Exception as e:
        print('USB reset failed (%s); continuing anyway' % e)
    time.sleep(2.5)


try:
    _reset_device()
    usb.open()
    factory_reset()
except RebootException:
    pass
