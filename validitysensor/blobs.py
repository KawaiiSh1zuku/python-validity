def __load_blob(blob: str) -> bytes:
    from .usb import usb

    if usb.usb_dev().idVendor == 0x138a:
        if usb.usb_dev().idProduct == 0x0090:
            from . import blobs_90 as blobs
        elif usb.usb_dev().idProduct == 0x0097:
            from . import blobs_97 as blobs
        elif usb.usb_dev().idProduct == 0x009d:
            from . import blobs_9d as blobs
    elif usb.usb_dev().idVendor == 0x06cb:
        if usb.usb_dev().idProduct == 0x009a:
            from . import blobs_9a as blobs
        elif usb.usb_dev().idProduct == 0x00a2:
            # 06cb:00a2 uses the same synaWudfBioUsb.dll as 138a:0090 (the DLL
            # does not branch on VID/PID at all), so it is the 0090 protocol
            # class and reuses the 0090 init/reset blobs. Do NOT use blobs_9a
            # here: 009a is a different driver package / fwext family.
            from . import blobs_90 as blobs

    globals()[blob] = getattr(blobs, blob)
    return globals()[blob]


init_hardcoded = lambda: __load_blob('init_hardcoded')
init_hardcoded_clean_slate = lambda: __load_blob('init_hardcoded_clean_slate')
reset_blob = lambda: __load_blob('reset_blob')
db_write_enable = lambda: __load_blob('db_write_enable')
