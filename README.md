# QtCustomWidgets

My custom widgets created for PySide6.

## Global Informations

 * Author: LostPy
 * Date: 2021-04-18
 * Version: 1.1
 
## Requirement:
 * Python 3.7+
 * Qt6
 * PySide6

## Installation

To install the last version:
```
pip install git+https://github.com/LostPy/QtCustomWidgets.git@Qt6
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
from Qt6CustomWidgets.<subpackage> import nameOfWidget
```

By example, to import the Progressbar from PySide6:
```py
from Qt6CustomWidgets.PySide6 import Progressbar
```
