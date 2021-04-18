from datetime import datetime
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QPoint, Qt, QDateTime
from PyQt5.QtGui import QImage, QPainter
from .ui.ui_graphicWidget import Ui_GraphicWidget

from PyQt5.QtChart import QChart
from PyQt5 import QtChart


class GraphicWidget(QWidget, Ui_GraphicWidget):
	retracted = pyqtSignal(bool)

	def __init__(self, title: str = "Untitled", parent=None):
		super(GraphicWidget, self).__init__(parent)
		self.setupUi(self)
		self.theme = QChart.ChartThemeLight
		self.set_chart()
		self.label.setText(title)
		self.old_height = self.height()

	@property
	def isRetracted(self):
		return self.graphicsView.isHidden()

	def set_chart(self, chart: QChart = None):
		if chart is None:
			chart = QChart()
		self.chart = chart
		self.chart.setTheme(self.theme)
		self.graphicsView.setChart(self.chart)

	def add_serie(self, serie):
		self.chart.addSeries(serie)

	def set_theme(self, theme):
		self.theme = theme
		self.chart.setTheme(self.theme)

	def add_line_serie(self, serie_name: str, x: list, y: list,
		datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm", legend: bool = True):
		line_serie = QtChart.QLineSeries(name=serie_name)
		for X, Y in zip(x, y):
			if isinstance(X, QDateTime) or isinstance(X, datetime):
				if isinstance(X, datetime):
					X = QDateTime(X)
				line_serie.append(X.toMSecsSinceEpoch(), Y)
			else:
				line_serie.append(X, Y)
		self.add_serie(line_serie)
		if len(self.chart.axes()) > 0:
			for axis in self.chart.axes():
				if axis.orientation() == Qt.Horizontal:
					if min(x) == axis.min() and max(x) == axis.max():
						line_serie.attachAxis(axis)
					elif datetime_axis:
						x_axis = QtChart.QDateTimeAxis()
						x_axis.setFormat(datetime_fmt)
						x_axis.setLabelsAngle(-20)
						self.chart.addAxis(x_axis, Qt.AlignTop)
						line_serie.attachAxis(x_axis)
					else:
						x_axis = QtChart.QValueAxis()
						x_axis.setRange(min(x) if len(x) > 0 else 0, max(x) if len(x) > 0 else 0)
						self.chart.addAxis(x_axis, Qt.AlignTop)
						line_serie.attachAxis(x_axis)

				else:
					if min(y) == axis.min() and max(y) == axis.max():
						line_serie.attachAxis(axis)
					else:
						y_axis = QtChart.QValueAxis()
						mini, maxi = min(y) if len(y) > 0 else 0, max(y) if len(y) > 0 else 0
						if mini == maxi:
							mini -= 0.5*mini
							maxi += 0.5*maxi
						y_axis.setRange(mini, maxi)
						self.chart.addAxis(y_axis, Qt.AlignRight)
						line_serie.attachAxis(y_axis)
		else:
			if datetime_axis:
				x_axis = QtChart.QDateTimeAxis()
				y_axis = QtChart.QValueAxis()
				x_axis.setFormat(datetime_fmt)
				x_axis.setLabelsAngle(-20)
				mini, maxi = min(y) if len(y) > 0 else 0, max(y) if len(y) > 0 else 0
				if mini == maxi:
					mini -= 0.5*mini
					maxi += 0.5*maxi
				y_axis.setRange(mini, maxi)
				self.chart.setAxisX(x_axis, line_serie)
				self.chart.setAxisY(y_axis, line_serie)
			else:
				self.chart.createDefaultAxes()
		self.chart.legend().setVisible(legend)

	def add_bar_serie(self, serie_name: str, sets: dict, xlabels: list = None, legend: bool = True):
		bar_serie = QtChart.QBarSeries(name=serie_name)
		self.add_serie(bar_serie)
		x_axis = QtChart.QBarCategoryAxis()
		y_axis = QtChart.QValueAxis()
		if xlabels is not None:
			x_axis.append(xlabels)
		else:
			x_axis.append[list(range(len(sets.values()[0])))]

		min_value = None
		max_value = None
		for set_name, data in sets.items():
			bar_set = QtChart.QBarSet(set_name)
			bar_set.append(data)
			bar_serie.append(bar_set)
			if min_value is None or min_value > min(data):
				min_value = min(data)
			if max_value is None or max_value < max(data):
				max_value = max(data)

		if min_value == max_value:
			min_value = 0
			max_value += max_value * 0.2
		y_axis.setRange(min_value, max_value)

		self.chart.addAxis(x_axis, Qt.AlignBottom)
		self.chart.addAxis(y_axis, Qt.AlignLeft)
		bar_serie.attachAxis(x_axis)
		bar_serie.attachAxis(y_axis)

		self.chart.legend().setVisible(legend)

	def add_barPercent_serie(self, serie_name: str, data: dict, categories: list, legend: bool = True):
		bar_serie = QtChart.QPercentBarSeries(name=serie_name)
		for label, values in data.items():
			bar_set = QtChart.QBarSet(label)
			bar_set.append(values)
			bar_serie.append(bar_set)
		self.add_serie(bar_serie)

		x_axis = QtChart.QBarCategoryAxis()
		x_axis.append(categories)
		self.chart.addAxis(x_axis, Qt.AlignBottom)
		bar_serie.attachAxis(x_axis)

		y_axis = QtChart.QValueAxis()
		self.chart.addAxis(y_axis, Qt.AlignLeft)
		bar_serie.attachAxis(y_axis)
		self.chart.legend().setVisible(legend)

	def add_pie_serie(self, serie_name: str, data: dict, legend: bool = True):
		pie_serie = QtChart.QPieSeries(name=serie_name)
		for label, value in data.items():
			pie_serie.append(label, value)
		self.add_serie(pie_serie)
		self.chart.legend().setVisible(legend)

	def add_scatter_serie(self, serie_name: str, x: list = [], y: list = [], marker=QtChart.QScatterSeries.MarkerShapeCircle,
		datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm", size: float = 10., legend: bool = True):
		scatter_serie = QtChart.QScatterSeries(name=serie_name)
		scatter_serie.setMarkerSize(size)
		scatter_serie.setMarkerShape(marker)
		for X, Y in zip(x, y):
			if isinstance(X, QDateTime) or isinstance(X, datetime):
				if isinstance(X, datetime):
					X = QDateTime(X)
				scatter_serie.append(X.toMSecsSinceEpoch(), Y)
			else:
				scatter_serie.append(X, Y)
		self.add_serie(scatter_serie)
		if len(self.chart.axes()) > 0:
			for axis in self.chart.axes():
				if axis.orientation() == Qt.Horizontal:
					if min(x) == axis.min() and max(x) == axis.max():
						scatter_serie.attachAxis(axis)
					elif datetime_axis:
						x_axis = QtChart.QDateTimeAxis()
						x_axis.setFormat(datetime_fmt)
						x_axis.setLabelsAngle(-20)
						self.chart.addAxis(x_axis, Qt.AlignTop)
						scatter_serie.attachAxis(x_axis)
					else:
						x_axis = QtChart.QValueAxis()
						x_axis.setRange(min(x) if len(x) > 0 else 0, max(x) if len(x) > 0 else 0)
						self.chart.addAxis(x_axis, Qt.AlignTop)
						scatter_serie.attachAxis(x_axis)

				else:
					if min(y) == axis.min() and max(y) == axis.max():
						scatter_serie.attachAxis(axis)
					else:
						y_axis = QtChart.QValueAxis()
						mini, maxi = min(y) if len(y) > 0 else 0, max(y) if len(y) > 0 else 0
						if mini == maxi:
							mini -= 0.5*mini
							maxi += 0.5*maxi
						y_axis.setRange(mini, maxi)
						self.chart.addAxis(y_axis, Qt.AlignRight)
						scatter_serie.attachAxis(y_axis)
		else:
			if datetime_axis:
				x_axis = QtChart.QDateTimeAxis()
				y_axis = QtChart.QValueAxis()
				x_axis.setFormat(datetime_fmt)
				x_axis.setLabelsAngle(-20)
				mini, maxi = min(y) if len(y) > 0 else 0, max(y) if len(y) > 0 else 0
				if mini == maxi:
					mini -= 0.5*mini
					maxi += 0.5*maxi
				y_axis.setRange(mini, maxi)
				self.chart.setAxisX(x_axis, scatter_serie)
				self.chart.setAxisY(y_axis, scatter_serie)
			else:
				self.chart.createDefaultAxes()
		self.chart.legend().setVisible(legend)

	def clear_chart(self):
		self.chart.removeAllSeries()
		for axis in self.chart.axes():
			self.chart.removeAxis(axis)

	def set_title(self, title: str):
		self.label.setText(title)

	def save_graphic(self, path: str) -> str:
		im = self.graphicsView.grab()
		im.save(path)
		return path

	@pyqtSlot()
	def on_toolButton_clicked(self):
		if self.graphicsView.isHidden():
			self.resize(self.width(), self.old_height)
			self.toolButton.setArrowType(Qt.DownArrow)
			self.graphicsView.show()
			self.retracted.emit(False)

		else:
			self.old_height = self.height()
			self.resize(self.width(), 40)
			self.toolButton.setArrowType(Qt.RightArrow)
			self.graphicsView.hide()
			self.retracted.emit(True)


