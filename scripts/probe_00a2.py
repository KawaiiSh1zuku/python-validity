#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe a Synaptics 06cb:00a2 fingerprint sensor and report its identity.

This script performs every initialization step that python-validity's normal
``open_common()`` does, EXCEPT ``Sensor.open()`` (which needs type-specific
calibration parameters that are only known for types 0x199 and 0xdb). It then
calls ``identify_sensor()`` and ``RomInfo.get()`` so you can learn the actual
``(major, minor, type)`` your hardware reports.

Why this exists
---------------
Static analysis of the Windows driver (synaWudfBioUsb.dll, which serves BOTH
138a:0090 and 06cb:00a2 from the exact same code path -- the DLL never branches
on VID/PID) shows 00a2 is the same protocol class as 0090. python-validity
already supports 0090, which reports sensor type 0x199. 00a2 is therefore very
likely also 0x199, but only the device itself can confirm that -- hence this
probe.

Prerequisites
-------------
1. Be root: ``sudo -i``
2. Place the firmware extension in the data dir::

       install -Dm644 6_07f_lenovo_sm_qm.xpfwext /var/run/python-validity/6_07f_lenovo_sm_qm.xpfwext

   (Copy it from the Lenovo Windows driver's WBF_Drivers folder.)

3. Run::

       python3 scripts/probe_00a2.py

   If the fwext was missing and got uploaded, the device reboots -- just run the
   script a second time.

Expected output
--------------
A block like::

    ================ IDENTIFY ================
      name      : '57K0 FM-3367-001   '
      major     : 0x0190
      version   : 0x004a
      type      : 0x0199
      rom_info  : RomInfo(...)
      >> type 0x199 is ALREADY SUPPORTED by Sensor.open() ...
    ==========================================

If the type is 0x199 (or 0xdb), python-validity works as-is -- proceed to
``fprintd-enroll``. If it is another type, report it so the matching calibration
parameters (key_calibration_line / calibration_frames / calibration_iterations)
can be added to Sensor.open().
"""
import logging
import sys

from validitysensor.init_data_dir import init_data_dir
from validitysensor.init_flash import init_flash
from validitysensor.flash import read_tls_flash
from validitysensor.tls import tls
from validitysensor.upload_fwext import upload_fwext
from validitysensor.usb import usb
from validitysensor.sensor import identify_sensor, RomInfo, RebootException

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def _is_reboot(e):
    return isinstance(e, RebootException) or 'Reboot' in str(e)


def main():
    init_data_dir()
    init_flash()
    usb.open()                       # finds 06cb:00a2 (now a SupportedDevice)
    usb.send_init()                  # sends init_hardcoded (reused from blobs_90)
    tls.parse_tls_flash(read_tls_flash())
    tls.open()

    try:
        upload_fwext()               # no-op if fwext already present; else upload+reboot
    except Exception as e:
        if _is_reboot(e):
            print('Firmware extension uploaded; the sensor rebooted.')
            print('Re-run this script now to identify the sensor.')
            return
        raise

    dev = identify_sensor()
    rom = RomInfo.get()

    print('================ IDENTIFY ================')
    print('  name      :', repr(dev.name))
    print('  major     : 0x%04x' % dev.major)
    print('  version   : 0x%04x' % dev.version)
    print('  type      : 0x%04x' % dev.type)
    print('  rom_info  :', repr(rom))
    if dev.type == 0x199:
        print('  >> type 0x199 is ALREADY SUPPORTED (line_update_type_1).')
        print('     python-validity should work as-is. Try: fprintd-enroll')
    elif dev.type == 0xdb:
        print('  >> type 0xdb is ALREADY SUPPORTED (line_update_type_2).')
        print('     python-validity should work as-is. Try: fprintd-enroll')
    else:
        print('  >> type 0x%04x is NOT yet supported.' % dev.type)
        print('     Report major=0x%04x version=0x%04x type=0x%04x so calibration'
              % (dev.major, dev.version, dev.type))
        print('     parameters can be added to Sensor.open() in sensor.py.')
    print('==========================================')

    # tidy exit: reboot so the sensor does not keep the TLS session open
    try:
        from validitysensor.sensor import reboot
        reboot()
    except RebootException:
        pass
    except Exception:
        pass


if __name__ == '__main__':
    main()
