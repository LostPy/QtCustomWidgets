# Project: QtCustomWidgets
# Author: LostPy

from setuptools import setup, find_packages

import Qt5CustomWidgets

with open('README.md', 'r', encoding='UTF-8') as f:
    README = f.read()


setup(
	name='Qt5CustomWidgets',
	version=Qt5CustomWidgets.__version__,
	author='LostPy',
	description="My Custom Widgets for PyQt5 and PySide2",
	long_description=README,
    package_dir = {'Qt5CustomWidgets': './Qt5CustomWidgets'},
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
        "Topic :: Qt5 :: PyQt5 :: PySide2",
    ],
    license='MIT',
    packages = find_packages()
    )
