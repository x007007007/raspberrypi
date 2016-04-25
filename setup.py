#!/usr/bin/env python
import os
import subprocess
from setuptools import setup, find_packages

git_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
def get_version():
    with open('version.txt') as fp:
        version = fp.readline()
        print(version)
        fp.seek(0)
        v = version.split('.')
        v[-1] = str(int(v[-1]) + 1)
        print v
        new_version = '.'.join(v)
    with open('version.txt', 'w') as fp:
        fp.write(new_version)
        return new_version

version = get_version()


requires = [
    'tornado',
    'django'
]

setup(
    name='raspberry-tools',
    version = version,
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
    author_email="x007007007@126.com",
    license='qiniu',
    url='https://github.com/qbox/net/tree/develop/cdn_quality',
    classifiers=[
        'Environment :: Raspberry',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
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