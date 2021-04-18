# Project: QtCustomWidgets
# Author: LostPy

from setuptools import setup, find_packages

import QtCustomWidgets

__doc__ = """My Custom Widgets for PyQt5"""


setup(
	name='osuData',
	version='1.20210418',
	author='LostPy',
	description="My Custom Widgets for PyQt5",
	long_description=__doc__,
    package_dir = {'QtCustomWidgets': './QtCustomWidgets'},
    package_data = {'': ['README.md']},
	include_package_data=True,
	url='',
	classifiers=[
        "Programming Language :: Python",
        "Development Status :: Functionnal - improvement in progress",
        "License :: MIT",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5+",
        "Topic :: PyQt5",
    ],
    license='MIT',
    packages = find_packages()
    )
