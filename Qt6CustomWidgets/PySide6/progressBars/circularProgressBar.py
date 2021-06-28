from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Property, Slot, QRect
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter


class CircularProgress(QWidget):
	def __init__(self, parent=None):
		super(CircularProgress , self).__init__(parent)

		self._value = 0
		self._minimum = 0
		self._maximum = 100
		self.width = 200
		self.height = 200
		self.progress_width = 10
		self.progress_rounded_cap = True
		self.progress_color = "#434c5e"
		self.font_family = "Arial"
		self.font_size = 20
		self.text_color = "#e5e9f0"
		self.enable_shadow = True
		self.update()
	
	def paintEvent(self, e: QPaintEvent):
		print("pain event")
		width = self.width - self.progress_width
		height = self.height - self.progress_width
		margin = self.progress_width / 2
		value = self._value * 360 / self._maximum

		paint = QPainter(self)
		paint.setRenderHint(QPainter.Antialiasing)

		rect = QRect(0, 0, self.width, self.height)
		paint.setPen(Qt.NoPen)
		paint.drawRect(rect)

		pen = QPen(QColor(self.progress_color))
		pen.setWidth(self.progress_width)
		if self.progress_rounded_cap:
			pen.setCapStyle(Qt.RoundCap)

		paint.setPen(pen)
		paint.drawArc(margin, margin, width, height, -90*16, -self._value*16)

		paint.end()


if __name__ == "__main__":
	import sys
	from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
	from PySide6.QtCore import Qt

	class Window(QWidget):
		def __init__(self):
			super().__init__(None)
			self.resize(600, 450)
			layout = QVBoxLayout()
			self.progress = CircularProgress(self)
			self.progress._value = 50
			self.slider = QSlider(Qt.Horizontal, self)

			layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter)
			layout.addWidget(self.slider, Qt.AlignCenter, Qt.AlignCenter)
			self.setLayout(layout)
			self.show()

	app = QApplication(sys.argv)
	w = Window()

	sys.exit(app.exec())
