#!/usr/bin/env python
import os
import subprocess
from setuptools import setup, find_packages


requires = [
    'tornado',
    'django',
    'picamera',
    'luma.oled',
    'RPi.GPIO'
]

setup(
    name='raspberry-tools',
    version = "1.2.3",
    install_requires=requires,
    packages=find_packages('src'),
    package_dir={
        "": "src"
    },
    package_data={
        '': ['*.txt', '*.rst', '*.md', '*.html', '*.json', '*.conf']
    },
    include_package_data=True,
    description="cdn_quality_net ({})".format(git_version),
    author = "xuxingci",
    author_email="x007007007@hotmail.com",
    license='qiniu',
    url='https://github.com/x007007007/raspberrypi/',
    classifiers=[
        'Environment :: Raspberry',
        'Intended Audience :: Developers',
        'Operating System :: Linux',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Raspberry',
    ],
    platforms = [
        "RaspberryPi", "Linux", "Unix"
    ],
    entry_points = {
        'console_scripts': [
            'keep_online=raspberrypi.server.cam:console_run',
            'cam2rtsp=raspberrypi.server.keep_online:console_run'
        ],
    }
)
