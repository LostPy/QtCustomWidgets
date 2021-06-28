# Project: QtCustomWidgets
# Author: LostPy

from setuptools import setup, find_packages

import Qt6CustomWidgets

with open('README.md', 'r', encoding='UTF-8') as f:
    README = f.read()


setup(
	name='Qt6CustomWidgets',
	version=Qt6CustomWidgets.__version__,
	author='LostPy',
	description="My Custom Widgets for PySide6",
	long_description=README,
    package_dir = {'Qt6CustomWidgets': './Qt6CustomWidgets'},
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
        "Topic :: Qt6 :: PySide6",
    ],
    license='MIT',
    packages = find_packages()
    )
