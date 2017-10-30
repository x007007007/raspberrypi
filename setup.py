#!/usr/bin/env python
import versioneer
from setuptools import setup, find_packages
cmdclass = versioneer.get_cmdclass()
from pyrequirements import get_requirements
get_requirements()
requires = [
    'tornado',
    'django',
    'picamera',
    # 'luma.oled',
    # 'RPi.GPIO'
]

setup(
    name='raspberry-tools',
    version = versioneer.get_version(),
    install_requires=requires,
    packages=find_packages('src'),
    package_dir={
        "": "src"
    },
    package_data={
        '': ['*.txt', '*.rst', '*.md', '*.html', '*.json', '*.conf']
    },
    include_package_data=True,
    description="RaspberryPi python code",
    author = "xuxingci",
    author_email="x007007007@hotmail.com",
    license='MIT',
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
