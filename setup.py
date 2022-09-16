
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
INSTALL_REQUIRES = [
    'setuptools<=57.4',
]
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
        'x007007007.djapp.local_net',
        'x007007007.djapp._models',
        'x007007007.djapp.local_net.admin',
        'x007007007.djapp.local_net.models',
    ],
    'package_dir': {'': 'src'},
    'package_data': {'': ['*']},
    'install_requires': INSTALL_REQUIRES,
    'extras_require': EXTRAS_REQUIRE,
    'python_requires': '>=3.10',

}


setup(**setup_kwargs)
