# QtCustomWidgets

My custom widgets created for PySide2.

## Global Informations

 * Author: LostPy
 * Date: 2021-04-18
 * Version: 1.0
 
## Requirement:
 * Python 3.7+
 * Qt5
 * PySide2

## Installation

To install the last version:
```
pip install git+https://github.com/LostPy/QtCustomWidgets.git@PySide2
```

## Add widgets to QtDesigner

To add custom widgets to QtDesigner (command line for Linux): `In progess`

## Widgets List

|Category|Name|Version add|Functional|Designer|
|--------|----|:---------:|:--------:|:------:|
|Buttons|ToggleButtonAnimated|1.0.20210418|✅|❌|
|Graphics|GraphicWidget|1.0.20210418|✅|❌|
|Display|ProgressBar|1.0.20210418|✅|❌|
|Display|CircularProgressBar|1.0.20210425|❌|❌|
|Display|PlainTextEditHandler|1.0.20210429|✅|❌|
|Dialog|dialogLogger|1.0.20210429|✅|❌|


## Import a Widget

To import a widget, you can use:
```py
from Qt5CustomWidgets import nameOfWidget
```

By example, to import the Progressbar:
```py
from Qt5CustomWidgets import Progressbar
```

