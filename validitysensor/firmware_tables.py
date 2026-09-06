"""Defines various constants for firmware files"""

from .usb import SupportedDevices

FIRMWARE_URIS = {
    SupportedDevices.DEV_90: {
        'driver': 'https://download.lenovo.com/pccbbs/mobiles/n1cgn08w.exe',
        'referral': 'https://support.lenovo.com/us/en/downloads/DS120491',
        'sha512': 'd839fa65adf4c952ecb4a5c4b2fc5b5bdedd8e02a421564bdc7fae1d281be4ea26fcde2333f2ab78d56cef0fdccce0a3cf429300b89544cdc9cfee6d0fe0db55'
    },
    SupportedDevices.DEV_97: {
        'driver': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'referral': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'sha512': 'a4a4e6058b1ea8ab721953d2cfd775a1e7bc589863d160e5ebbb90344858f147d695103677a8df0b2de0c95345df108bda97196245b067f45630038fb7c807cd'
    },
    SupportedDevices.DEV_9a: {
        'driver': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'referral': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'sha512': 'a4a4e6058b1ea8ab721953d2cfd775a1e7bc589863d160e5ebbb90344858f147d695103677a8df0b2de0c95345df108bda97196245b067f45630038fb7c807cd'
    },
    SupportedDevices.DEV_9d: {
        'driver': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'referral': 'https://download.lenovo.com/pccbbs/mobiles/nz3gf07w.exe',
        'sha512': 'a4a4e6058b1ea8ab721953d2cfd775a1e7bc589863d160e5ebbb90344858f147d695103677a8df0b2de0c95345df108bda97196245b067f45630038fb7c807cd'
    },
    SupportedDevices.DEV_a2: {
        # TODO: fill in the exact Lenovo download URL and the SHA-512 of the
        # downloaded installer .exe (the tool checks the *exe* hash, then
        # extracts the fwext via innoextract). The fwext shipped with this
        # ThinkPad S2 2018 driver package is 6_07f_lenovo_sm_qm.xpfwext
        # (sha512 of the fwext file itself:
        #  f5cf6425fabffe1ad3fd3fcf6439b166c60d5f3660c4c0969c17768481233dbc
        #  4fa2fb73d51b7d2f498d461a7f4e334f6c19bb8eca3d67cb0afdfe73b6963cad).
        # Until the URL is known, copy the fwext manually:
        #   cp 6_07f_lenovo_sm_qm.xpfwext /var/run/python-validity/
        'driver': '',
        'referral': '',
        'sha512': ''
    }
}

FIRMWARE_NAMES = {
    SupportedDevices.DEV_90: '6_07f_Lenovo.xpfwext',
    SupportedDevices.DEV_97: '6_07f_lenovo_mis_qm.xpfwext',
    SupportedDevices.DEV_9a: '6_07f_lenovo_mis_qm.xpfwext',
    SupportedDevices.DEV_9d: '6_07f_lenovo_mis_qm.xpfwext',
    SupportedDevices.DEV_a2: '6_07f_lenovo_sm_qm.xpfwext'
}
