#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only diagnostic for a 06cb:00a2 sensor.

Prints the on-chip flash IC (name + total size) and current partition table,
plus the fingerprint database info and user/finger list. It does NOT factory
reset and does NOT enroll, so it is safe to run on a Windows-prepared device.

Run with the dbus service stopped (otherwise the device is busy):

    sudo systemctl stop python3-validity
    sudo python3 /usr/share/python-validity/diag_00a2.py

What to look for in the output
-------------------------------
* FLASH / IC size:
    - < 0xd0000  -> a later factory-reset MUST use the 0090 layout (smaller
                   template DB 0x30000); the default layout (0x80000) would
                   run past the chip end.
    - >= 0xd0000 -> default layout is fine.
* DATABASE:
    - users/fingers carried over from Windows -- if enroll fails with 0x0401
      while these are present, a factory-reset (which clears them) is the
      usual fix.
"""
import logging

from validitysensor.init_data_dir import init_data_dir
from validitysensor.init_flash import init_flash
from validitysensor.flash import read_tls_flash, get_flash_info
from validitysensor.tls import tls
from validitysensor.usb import usb
from validitysensor.db import db
from validitysensor.sensor import reboot, RebootException

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main():
    init_data_dir()
    usb.open()
    init_flash()                       # early-returns when already partitioned
    usb.send_init()
    tls.parse_tls_flash(read_tls_flash())
    tls.open()

    print('================ FLASH ================')
    info = get_flash_info()
    print('  IC name    :', info.ic.name)
    print('  IC size    : 0x%x (%d KB)' % (info.ic.size, info.ic.size // 1024))
    print('  blocks     : %d' % info.blocks)
    print('  block size : 0x%x' % info.blocksize)
    print('  partitions : %d' % len(info.partitions))
    for p in info.partitions:
        print('    id=0x%02x type=0x%02x access=0x%03x offset=0x%08x size=0x%08x'
              % (p.id, p.type, p.access_lvl, p.offset, p.size))

    if info.ic.size < 0xd0000:
        print('  >> flash < 0xd0000: a factory-reset MUST use the 0090 layout')
        print('     (template DB 0x30000), NOT the default 0x80000.')
    elif info.ic.size < 0x80000:
        print('  >> flash very small; neither shipped layout fits -- needs custom.')
    else:
        print('  >> flash >= 0xd0000: default layout (template DB 0x80000) is OK.')

    print('================ DATABASE ================')
    try:
        di = db.db_info()
        print('  total   : 0x%x (%d KB)' % (di.total, di.total // 1024))
        print('  used    : 0x%x' % di.used)
        print('  free    : 0x%x' % di.free)
        print('  records : %d' % di.records)
        print('  roots   : %s' % di.roots)
    except Exception as e:
        print('  db_info() failed:', repr(e))

    print('  --- users / fingers ---')
    try:
        db.dump_all()
    except Exception as e:
        print('  dump_all() failed:', repr(e))
    print('==========================================')

    # tidy exit
    try:
        reboot()
    except RebootException:
        pass
    except Exception:
        pass


if __name__ == '__main__':
    main()
