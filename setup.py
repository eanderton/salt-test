#!/usr/bin/env python

import setuptools
import subprocess
from setuptools.command.develop import develop as setuptools_develop
from setuptools.command.test import test as setuptools_test
from salt_test.version import __VERSION__

# shim to install dev depenedencies on 'setup.py develop'
class ExtDevelopCommand(setuptools_develop):
    def install_for_development(self):
        from distutils import log
        setuptools_develop.install_for_development(self)
        log.info('\nInstalling development dependencies')
        reqs = ' '.join(self.distribution.extras_require.get('develop', []))
        proc = subprocess.Popen('pip install ' + reqs, shell=True)
        proc.wait()


setuptools.setup(
    name='salt-test',
    version=__VERSION__,
    description='Salt test utility',
    long_description=open('README.md').read().strip(),
    author='Eric Anderton',
    author_email='eric.t.anderton@gmail.com',
    url='http://github.com/eanderton/salt-test',
    packages=['salt_test'],
    test_suite='tests',
    install_requires=[
        'salt',
        'pyzmq',
        'backports.tempfile',
    ],
    extras_require={
        'develop': [
            'coverage',
            'mock',
        ],
    },
    cmdclass={
        'develop': ExtDevelopCommand,
    },
    entry_points={
        'console_scripts': [
            'salt-test=salt_test.cli:main',
        ],
    },
    license='MIT License',
    zip_safe=False,
    keywords='salt saltstack continuous-integration ci test testing',
    classifiers=[
        'Packages'
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ])
