"""
A custom progress bar with a custom color.
"""

from math import sqrt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import (
	Qt, QSize, QPoint, QPointF, QRectF,
	QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
	pyqtSignal, pyqtSlot, pyqtProperty)
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter


class ProgressBar(QWidget):

	valueChanged = pyqtSignal(int)

	def __init__(self, orientation=Qt.Horizontal, minimum: int = 0, maximum: int = 100, borderwidth: int = 3,
		bar_color="#ffffff", color_loaded="#0ca678", pen_color="#212529", text_color='#000000',
		rounding: float = 0., showPercent: bool = True, showValue: bool = False, parent=None):
		super(ProgressBar, self).__init__(parent)
		self._penColor = QColor(pen_color)
		self._textColor = QColor(text_color)
		self._barColor = QColor(bar_color)
		self._loadedColor = QColor(color_loaded)
		self._borderWidth = borderwidth

		self._value = minimum
		self._minimum = minimum
		self._maximum = maximum

		self.orientation = orientation
		self._rounding = rounding
		self._showPercent = showPercent
		self._showValue = showValue

	@pyqtProperty(int)
	def minimum(self):
		return self._minimum

	@minimum.setter
	def minimum(self, value: int):
		if value < self.maximum:
			self._minimum = value
			self.value = self._value

	@pyqtProperty(int)
	def maximum(self):
		return self._maximum

	@maximum.setter
	def maximum(self, value: int):
		if value >= self.minimum:
			self._maximum = value
			self.value = self._value

	@pyqtProperty(int)
	def value(self):
		return self._value

	@value.setter
	def value(self, value: int):
		if self.minimum <= value <= self.maximum:
			self._value = value
		elif self.minimum > value:
			self._value = self.minimum
		else:
			self._value = self.maximum
		self.valueChanged.emit(self._value)
		self.update()

	@pyqtProperty(float)
	def percent(self):
		return ((self.value - self.minimum) / abs(self.maximum - self.minimum))*100

	@percent.setter
	def percent(self, value: float):
		self.value = ((value - self.minimum) * abs(self.maximum - self.minimum)) / 100

	@pyqtProperty(QColor)
	def penColor(self):
		return self._penColor

	@penColor.setter
	def penColor(self, color: QColor):
		self._penColor = QColor(color)

	@pyqtProperty(QColor)
	def barColor(self):
		return self._barColor

	@barColor.setter
	def barColor(self, color: QColor):
		self._barColor = QColor(color)

	@pyqtProperty(QColor)
	def loadedColor(self):
		return self._loadedColor

	@loadedColor.setter
	def loadedColor(self, color: QColor):
		self._loadedColor = QColor(color)

	@pyqtProperty(QColor)
	def textColor(self):
		return self._textColor

	@textColor.setter
	def textColor(self, color: QColor):
		self._textColor = QColor(color)

	@pyqtProperty(int)
	def borderWidth(self):
		return self._borderWidth

	@borderWidth.setter
	def borderWidth(self, value: int):
		self._borderWidth = value

	@pyqtProperty(float)
	def roundingCorner(self):
		return self._rounding

	@roundingCorner.setter
	def roundingCorner(self, value: float):
		self._rounding = value

	@pyqtProperty(bool)
	def showPercent(self):
		return self._showPercent

	@showPercent.setter
	def showPercent(self, show: bool):
		self.update()
		self._showPercent = show

	@pyqtProperty(bool)
	def showValue(self):
		return self._showValue

	@showValue.setter
	def showValue(self, value: bool):
		self.update()
		self._showValue = value

	def setMinimum(self, value: int):
		self.minimum = value

	def setMaximum(self, value: int):
		self.maximum = value

	def setRange(self, mini: int, maxi: int):
		if mini < maxi:
			self.minimum = mini
			self.maximum = maxi

	@pyqtSlot(int)
	def setValue(self, value: int):
		self.value = value

	@pyqtSlot(int)
	def increaseValue(self, value: int):
		self.value += value

	@pyqtSlot(int)
	def discreaseValue(self, value: int):
		self.value -= value

	@pyqtSlot(bool)
	def setShowPercent(self, show_percent: bool):
		self.showPercent = show_percent

	@pyqtSlot(bool)
	def setShowValue(self, show_value: bool):
		self.showValue = show_value

	def draw_bar(self, painter: QPainter):
		painter.save()

		contRect = self.contentsRect()
		handleRadius = round(0.3 * contRect.height())
		barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
		barRect.moveCenter(contRect.center())

		painter.setBrush(QBrush(self.barColor))
		painter.drawRoundedRect(barRect, self._rounding, self._rounding)

		painter.restore()
		return barRect

	def draw_loaded_bar(self, painter: QPainter, barRect: QRectF):
		painter.save()
		width_loaded = self._rounding*2 if self.percent/100 == 0 else self._rounding*2 + (barRect.width() - self._rounding*2) * (self.percent/100)
		loadedRect = QRectF(barRect.x(), barRect.y(), width_loaded, barRect.height())

		painter.setBrush(QBrush(self.loadedColor))
		painter.setPen(Qt.NoPen)
		painter.drawRoundedRect(loadedRect, self._rounding, self._rounding)
		painter.restore()
		return loadedRect

	def draw_text(self, painter: QPainter, barRect: QRectF):
		painter.save()

		font = painter.font()
		size_font = barRect.height() // 3
		if size_font < 1:
			size_font = 1
		else:
			size_font = size_font if size_font < 30 else 30
		font.setPixelSize(int(size_font))

		pen = QPen(self._textColor)
		pen.setWidth(2)
		painter.setPen(pen)
		painter.setFont(font)


		percent_rounded = round(self.percent, 2) if self._showPercent else None
		len_percent = (len(str(percent_rounded)) + 2) * (size_font / 4) if self._showPercent else None
		len_value = (len(str(self._value)) + len(str(self._maximum)) + 3) * (size_font / 4) if self._showValue else None
		X, Y = barRect.x() + barRect.width()/2, 1.1*barRect.y() + barRect.height()/2
		textPoint = QPointF(X, Y)

		if self._showPercent and self._showValue:
			textPoint.setX(X - len_percent)
			textPoint.setY(Y - 0.5*size_font)
			painter.drawText(textPoint, f"{percent_rounded} %")
			textPoint.setX(X - len_value)
			textPoint.setY(Y + 0.5*size_font)
			painter.drawText(textPoint, f"{self._value} / {self._maximum}")
		elif self._showValue:
			textPoint.setX(X - len_value)
			painter.drawText(textPoint, f"{self._value} / {self._maximum}")
		elif self._showPercent:
			textPoint.setX(X - len_percent)
			painter.drawText(textPoint, f"{percent_rounded} %")
		painter.restore()

	def paintEvent(self, e: QPaintEvent):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		pen = QPen(self._penColor)
		pen.setWidth(self._borderWidth)
		painter.setPen(pen)

		barRect = self.draw_bar(painter)
		self.draw_loaded_bar(painter, barRect)

		if self._showPercent or self._showValue:
			self.draw_text(painter, barRect)
		painter.end()


if __name__ == '__main__':
	import sys
	import time
	from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton
	from PyQt5.QtCore import Qt

	class Widget(QWidget):
		def __init__(self):
			super().__init__()
			self.progress = ProgressBar(rounding=0., showPercent=True, showValue=True, parent=self)
			self.progress.setRange(20, 200)
			self.slider = QSlider(Qt.Horizontal, self)
			self.slider.setRange(20, 200)
			self.button = QPushButton("Add 5", self)
			layout = QVBoxLayout()
			layout.addWidget(self.progress)
			layout.addWidget(self.slider)
			layout.addWidget(self.button)
			self.setLayout(layout)
			self.button.clicked.connect(self.add_five)
			self.slider.valueChanged.connect(self.on_slider_valueChanged)

		def on_slider_valueChanged(self, value: int):
			self.progress.setValue(value)

		def add_five(self):
			self.progress.increaseValue(5)
			self.slider.setValue(self.progress.value)


	app = QApplication(sys.argv)
	w = Widget()
	w.setGeometry(100, 100, 100, 20)
	w.show()
	sys.exit(app.exec_())

