# QtCustomWidgets

My custom widgets created for PyQt5 and PySide2.

## Global Informations

 * Author: LostPy
 * Date: 2021-04-18
 * Version: 1.0
 
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
