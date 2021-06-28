# Project: QtCustomWidgets
# Author: LostPy

from setuptools import setup, find_packages

import QtCustomWidgets

with open('README.md', 'r', encoding='UTF-8') as f:
    README = f.read()


setup(
	name='QtCustomWidgets',
	version=QtCustomWidgets.__version__,
	author='LostPy',
	description="My Custom Widgets for PyQt5",
	long_description=README,
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
        "Programming Language :: Python :: 3.7+",
        "Topic :: PyQt5",
    ],
    license='MIT',
    packages = find_packages()
    )
