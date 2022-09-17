
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
EXTRAS_REQUIRE = {
    'test': [
        'pytest',
        'pytest-cov[all]',
        'pytest-django',
        'pytest-asyncio',
    ],
    'lint': [
        'black',
        'flake8',
    ],
    'dj': [
        'django',
        'djangorestframework',
        'django-filter',
    ],
    'dj-ch': [
        'django',
        'djangorestframework',
        'django-filter',
        'channels',
    ],
    'dj-raspberrypi': [
        'django',
        'djangorestframework',
        'django-filter',
        'channels',
        'zeroconf>=0.39.1',
    ],
    'dj-raspberrrypi': [
        'netifaces>=0.11.0',
    ],
}

setup_kwargs = {
    'name': 'x007007007-respberrypi',
    'version': '0.1.0',
    'description': '',
    'long_description': long_description,
    'license': 'MIT',
    'author': '',
    'author_email': 'xingci.xu <x007007007@hotmail.com>',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': [
        'x007007007',
        'x007007007.RPi',
        'x007007007.RPi.dirver',
        'x007007007.djserver.raspberrypi',
        'x007007007.djserver.raspberrypi.settings',
        'x007007007.djapp.localnet',
        'x007007007.djapp.raspberry',
        'x007007007.djapp._models',
        'x007007007.djapp.localnet.nameserver',
        'x007007007.djapp.localnet.zeroconf',
        'x007007007.djapp.localnet.nameserver.migrations',
        'x007007007.djapp.localnet.nameserver.admin',
        'x007007007.djapp.localnet.nameserver.component',
        'x007007007.djapp.localnet.nameserver.models',
        'x007007007.djapp.localnet.nameserver.management.commands',
        'x007007007.djapp.localnet.zeroconf.migrations',
        'x007007007.djapp.localnet.zeroconf.admin',
        'x007007007.djapp.localnet.zeroconf.component',
        'x007007007.djapp.localnet.zeroconf.models',
        'x007007007.djapp.localnet.zeroconf.management.commands',
        'x007007007.djapp.raspberry.net',
        'x007007007.djapp.raspberry.net.models',
    ],
    'package_dir': {'': 'src'},
    'package_data': {'': ['*']},
    'extras_require': EXTRAS_REQUIRE,
    'python_requires': '>=3.10',

}


setup(**setup_kwargs)
