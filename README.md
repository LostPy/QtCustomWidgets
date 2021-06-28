# QtCustomWidgets

My custom widgets created for PyQt5 and PySide2.

## Global Informations

 * Author: LostPy
 * Date: 2021-04-18
 * Version: 1.1
 
## Requirement:
 * Python 3.7+
 * Qt5
 * PySide2
 * PyQt5

## Installation

To install the last version:
```
pip install git+https://github.com/LostPy/QtCustomWidgets.git@Qt5
```

## Add widgets to QtDesigner (PyQt5)

To add custom widgets to QtDesigner (command line for Linux):
 1. Create a directory `python` in `path/of/qt5/plugins/designer/` (For Linux, it's probably `/usr/lib/x86_64-linux-gnu/qt5/plugins/designer`). Use the command line: `sudo mkdir /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python`.
 2. Copy the directory `QtCustomWidgets` in `path/of/qt5/plugins/designer/python/`. In this directory, use the command line: `sudo cp -r ./QtCustomWidgets /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python/`.
 3. Copy the files of `./plugins` directory (in this directory), in `path/of/qt5/plugins/designer/python`. Use the command line: `sudo cp ./plugins/*.py /usr/lib/x86_64-linux-gnu/qt5/plugins/designer/python/`.
 4. Run designer: `designer` or `designer-qt5`

## Widgets List

|Category|Name|Version add|Functional|QtDesigner|
|--------|----|:---------:|:--------:|:--------:|
|Buttons|ToggleButtonAnimated|1.0.20210418|✅|✅|
|Graphics|GraphicWidget|1.0.20210418|✅|❌|
|Display|ProgressBar|1.0.20210418|✅|✅|
|Display|CircularProgressBar|1.0.20210425|❌|❌|
|Display|PlainTextEditHandler|1.0.20210429|✅|❌|
|Dialog|dialogLogger|1.0.20210429|✅|❌|


## Import a Widget

To import a widget, you can use:
```py
from Qt5CustomWidgets.<subpackage> import nameOfWidget
```

By example, to import the Progressbar from PySide2:
```py
from Qt5CustomWidgets.PySide2 import Progressbar
```
