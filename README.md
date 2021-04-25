# QtCustomWidgets

My custom widgets created for QtDesigner and PyQt5.

## Global Informations

 * Author: LostPy
 * Date: 2021-04-18
 * Version: 0.1
 
## Requirement:
 * Python 3.7+
 * Qt5
 * PyQt5
 * For someone widgets: PyQtGraph

## Installation

To install the last version:
 * On Window or a virtual environment: `pip install git+https://github.com/LostPy/QtCustomWidgets.git@main`
 * On Linux: `pip3 install git+https://github.com/LostPy/QtCustomWidgets.git@main`

## Add widgets to QtDesigner

To add custom widgets to QtDesigner (command line for Linux):
 1. Create a directory `python` in `path/of/qt5/plugins/designer/` (For Linux, it's probably `/usr/lib/x86_64-linux-gnu/qt5/plugins/designer`). Use the command line: `sudo mkdir /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python`.
 2. Copy the directory `QtCustomWidgets` in `path/of/qt5/plugins/designer/python/`. In this directory, use the command line: `sudo cp -r ./QtCustomWidgets /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python/`.
 3. Copy the files of `./plugins` directory (in this directory), in `path/of/qt5/plugins/designer/python`. Use the command line: `sudo cp ./plugins/*.py /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python/`.
 4. Run designer: `designer` or `designer-qt5`

## Widgets List

|Category|Name|Version add|Functional|
|--------|----|:---------:|:--------:|
|buttons|ToggleButtonAnimated|1.20210418|✅|
|dataVisualization|GraphicWidget|1.20210418|✅|
|progressBar|ProgressBar|1.20210418|✅|
|progressBar|CircularProgressBar|1.20210425|❌|


## Import a Widget

To import a widget, you can use:
```py
from QtCustomWidgets import nameOfWidget
```

By example, to import the Progressbar:
```py
from QtCustomWidgets import Progressbar
```

