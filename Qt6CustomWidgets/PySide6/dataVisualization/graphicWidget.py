"""
Ui pour le système de surveillance du radar UHF
"""

from datetime import datetime
from numpy import nan

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, Signal, QPoint, Qt, QDateTime,Property
from PySide6.QtGui import QImage, QPainter
from PySide6.QtCharts import QChart
from PySide6 import QtCharts

from .ui.ui_graphicWidget import Ui_GraphicWidget


class GraphicWidget(QWidget, Ui_GraphicWidget):
	"""A Widget to display a graph.
	It's a subclass of QWidget.

	Public Attributs
	---------
	chartView : QChartView
		The QChartView use to display the chart.
	chart : QChart
		The chart with the differents series to display
	theme : ChartTheme
		The theme use for this chart

	Public Methods
	-------
	set_chart
		Set a chart to the QChartView
	add_series
		Add a series to the chart
	set_theme
		Set a new theme to the chart
	set_title
		Set a new title to the graph
	add_line_series
		Add a line series to the chart
	add_scatter_series
		Add a scatter series to the chart
	add_bar_series
		Add a bar series to the chart
	add_barPercent_series
		Add a percent bar series to the chart
	add_pie_series
		Add a pie series to the chart
	clear_chart
		Clear all series of chart
	save
		Saves the QChartView
	
	Protected Attributes
	--------------------
	_old_height : int
		The former height of the widget before it was retracted

	Protected Methods
	-----------------
	_create_x_axis
		Method to create and setup a X axis (Create a QValueAxis or QDatetime axis)
	_create_y_axis
		Method to create and setup a Y axis (Create a QValueAxis or QDatetime axis)
	_same_range
		Method to test if two ranges are similar
	_largest_range
		Method to get a range which included all ranges passed in parameters.
	_setup_axis
		Method to setup axis of a QXYSeries
	_add_points_data
		Methods to add points data to a QXYSeries
	_setup_bar_series
		Methods to setup bar set and axis of a QAbstractBarSeries

	Desctiptors
	-----------
	isRetracted : bool
		Return if self.graphicView is hidden or not

	PyQt Property
	-------------
	title : str
		The title of graph

	Signals
	-------
	retracted
		A signal emitted when the GraphicWidget is retracted.
		Parameters:
			retracted : bool
				A boolean to specify if the graphicWidget is retracted or not.
	"""
	retracted = Signal(bool)

	def __init__(self, parent=None, title: str = "Untitled"):
		"""Initialize an instance of GraphicWidget

		Parameters
		---------
		parent : QWidget
			The parent widget of the instance of GraphicWidget
		OPTIONAL[title] : str
			The title of graph
			Default: "Untitled"
		"""
		super(GraphicWidget, self).__init__(parent)
		self.setupUi(self)
		self.theme = QChart.ChartThemeLight
		self.set_chart()
		self.label.setText(title)
		self._old_height = self.height()

	@property
	def isRetracted(self):
		"""A property to know if the widget is retracted or not

		Returns
		-------
		isRetracted : bool
			Return if self.graphicView is hidden or not
		"""
		return self.chartView.isHidden()

	@Property(str)
	def title(self):
		"""The title of graph
		
		Returns
		-------
		title : str
			The current title of graph
		"""
		return self.label.text()

	@title.setter
	def title(self, new_title: str):
		"""Set a new title for the graph
		
		Parameters
		----------
		new_title : str
			The new title
		"""
		self.label.setText(new_title)

	def set_chart(self, chart: QChart = None):
		"""Set a char to QChartView

		Parameters
		---------
		OPTIONAL[chart] : Union[QChart, None]
			the chart to set, if None: set an empty chart

		Returns
		-------
		None
		"""
		if chart is None:
			chart = QChart()
		self.chart = chart
		self.chart.setTheme(self.theme)
		self.chartView.setChart(self.chart)

	def add_series(self, series):
		"""Add a series to the chart of QChartView

		Parameters
		---------
		series : QAbstractSerie
			The series to add

		Returns
		-------
		None
		"""
		self.chart.addSeries(series)

	def set_theme(self, theme):
		"""Set a theme to the chart

		Parameters
		---------
		theme : ChartTheme
			The theme to set to the chart
		Returns
		-------
		None
		"""
		self.theme = theme
		self.chart.setTheme(self.theme)

	def set_title(self, title: str):
		"""Set a new title for the GraphicWidget

		Parameters
		---------
		title : str
			The new title

		Returns
		-------
		None
		"""
		self.title = title

	def _create_x_axis(self, x_range: tuple = (0, 0), y_range: tuple = (0, 0),
		x_axis_align: int = Qt.AlignBottom, y_axis_align: int = Qt.AlignLeft, labels_angle: int = 0,
		datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm"):
		"""Method to create axis. These axis are added to the chart.

		Parameters
		---------
		OPTIONAL[x_range] : Tuple[Union[int, float], Union[int, float]]
			The x range : the first value must be the minimum value of x axis and the second the maximum value of x axis.
			Default: (0, 0)
		OPTIONAL[x_axis_align] : int, a Qt alignment flag
			The alignment flag to x axis.
			Default: Qt.AlignBottom
		OPTIONAL[labels_angle] : int
			Angle for the labels
			Default: 0
		OPTIONAL[datetime_axis] : bool
			If True, the x axis is a QDatetimeAxis, it's not necessary to specify a x range.
			Default: False
		OPTIONAL[datetime_fmt] : str
			The datetime format, only use if datetime_axis is True.
			Default: "yyyy-MM-dd h:mm"

		Returns
		-------
		x_axis : Union[QValueAxis, QDatetimeAxis]
			The x axis created
		"""

		if datetime_axis:
			x_axis = QtCharts.QDateTimeAxis()
			x_axis.setFormat(datetime_fmt)
			if isinstance(x_range[0], QDateTime) and isinstance(x_range[1], QDateTime):
				x_axis.setRange(x_range[0], x_range[1])
		else:
			x_axis = QtCharts.QValueAxis()
			x_axis.setRange(x_range[0], x_range[1])
		x_axis.setLabelsAngle(labels_angle)

		self.chart.addAxis(x_axis, x_axis_align)
		return x_axis

	def _create_y_axis(self, y_range: tuple = (0, 0), y_axis_align: int = Qt.AlignLeft, labels_angle: int = 0,
						datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm"):
		"""Method to create a y axis. This axis is added to the chart.

		Parameters
		---------
		OPTIONAL[y_range] : Tuple[Union[int, float, QDateTime], Union[int, float, QDateTime]]
			The y range : the first value must be the minimum value of y axis and the second the maximum value of y axis.
			Default: (0, 0)
		OPTIONAL[y_axis_align] : int, a Qt alignment flag
			The alignment flag to y axis.
			Default: Qt.AlignLeft
		OPTIONAL[labels_angle] : int
			Angle for the labels
			Default: 0
		OPTIONAL[datetime_axis] : bool
			If True, the x axis is a QDatetimeAxis, it's not necessary to specify a x range.
			Default: False
		OPTIONAL[datetime_fmt] : str
			The datetime format, only use if datetime_axis is True.
			Default: "yyyy-MM-dd h:mm"

		Returns
		-------
		y_axis : QValueAxis
			The y axis created
		"""
		if datetime_axis:
			y_axis = QtCharts.QDateTimeAxis()
			y_axis.setFormat(datetime_fmt)
			if isinstance(y_range[0], QDateTime) and isinstance(y_range[1], QDateTime):
				y_axis.setRange(y_range[0], y_range[1])
		else:
			y_axis = QtCharts.QValueAxis()
			y_axis.setRange(y_range[0], y_range[1])
		y_axis.setLabelsAngle(labels_angle)

		self.chart.addAxis(y_axis, y_axis_align)
		return y_axis

	def _same_range(self, axis, range_: tuple, tolerance: float = 0.3):
		"""Compare the range of axis and the range of range_ with a tolerance.

		Parameters
		---------
		axis : QtCharts.QAbstractAxis
			The axis to compare
		range_ : Tuple[Union[int, float], Union[int, float]]
			The range to compare with the range of axis
		OPTIONAL[tolerance] : float, greater than 0
			The tolerance to use
			Default: 0.2

		Returns
		-------
		result : bool
			Return if axis range == range_ with the tolerance specified.
		"""
		def convert_datetime_to_ms(value):
			if isinstance(value, QDateTime):
				return value.toMSecsSinceEpoch()
			elif isinstance(value, datetime):
				return value.timestamp() * 1000
			return value

		axis_min, axis_max = convert_datetime_to_ms(axis.min()), convert_datetime_to_ms(axis.max())
		min_value, max_value = convert_datetime_to_ms(range_[0]), convert_datetime_to_ms(range_[1])

		tolerance_value = tolerance * abs(axis_max - axis_min)
		return axis_min - tolerance_value <= min_value <= axis_min + tolerance_value and\
				axis_max - tolerance_value <= max_value <= axis_max + tolerance_value

	def _largest_range(self, range_1: tuple, *other_ranges):
		"""Find a range wich included all ranges passed in parameters.

		Parameters
		---------
		range_1 : Tuple[Union[int, float], Union[int, float]]
			A range which must be included in the larger range.
		OPTIONAL[*other_ranges] : Tuple[Union[int, float], Union[int, float]]
			The other ranges

		Returns
		-------
		new_min : Union[int, float]
			The new min value of range
		new_max : Union[int, float]
			The new max value of range
		"""
		new_min, new_max = min((range_[0] for range_ in other_ranges)), max((range_[1] for range_ in other_ranges))
		return new_min, new_max

	def _setup_axis(self, series, x, y, datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm",
									legend: bool = True):
		"""Setup axis for a QXYSeries.

		Parameters
		---------
		series : QXYSeries
			The series to set the axis
		x : Iterable
			Data for X axis
		y : Iterable
			Data for Y axis
		OPTIONAL[datetime_axis] : bool
			If True, the X axis is a QDatetimeAxis else a QValueAxis
			Default: False
		OPTIONAL[datetime_fmt] : str
			If datetime_axis is True, specify the datetime format.
			Default: "yyyy-MM-dd h:mm"
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		if len(self.chart.axes()) > 0 and len(x) > 0 and len(y) > 0:
			x_range = (min(x), max(x))
			y_range = (min(y), max(y))
			for axis in self.chart.axes():
				if axis.orientation() == Qt.Horizontal:
					if self._same_range(axis, x_range):
						axis.setRange(*self._largest_range((axis.min(), axis.max()), x_range))
						series.attachAxis(axis)
					else:
						x_axis = self._create_x_axis(x_range, Qt.AlignTop, labels_angle=-20, datetime_axis=datetime_axis, datetime_fmt=datetime_fmt, x_axis_align=Qt.AlignTop)
						series.attachAxis(x_axis)

				else:

					if self._same_range(axis, y_range):
						axis.setRange(*self._largest_range((axis.min(), axis.max()), y_range))
						series.attachAxis(axis)
					else:
						mini = 0.5*y_range[0] if y_range[0] == y_range[1] else y_range[0]
						maxi = 0.5*y_range[1] if y_range[0] == y_range[1] else y_range[1]
						y_axis = self._create_y_axis((mini, maxi), y_axis_align=Qt.AlignRight)
						series.attachAxis(y_axis)

		elif len(x) > 0 and len(y) > 0:
			x_range = (min(x), max(x))
			y_range = (min(y), max(y))
			x_angle_labels = 0 if len(str(x_range[1])) < 5 else -20
			if datetime_axis:
				x_axis = self._create_x_axis(x_range, Qt.AlignBottom, datetime_axis=datetime_axis, datetime_fmt=datetime_fmt, labels_angle=x_angle_labels)
				series.attachAxis(x_axis)
				mini = 0.5*y_range[0] if y_range[0] == y_range[1] else y_range[0]
				maxi = 0.5*y_range[1] if y_range[0] == y_range[1] else y_range[1]
				y_axis = self._create_y_axis((mini, maxi), y_axis_align=Qt.AlignLeft)
				series.attachAxis(y_axis)
			else:
				self.chart.createDefaultAxes()
		self.chart.legend().setVisible(legend)

	def _add_points_data(self, series, x: list, y: list):
		"""Add points data to the series (a QXYSeries).

		Parameters
		---------
		series : QXYSeries
			The line or scatter series
		x : Iterable
			The X-coordinates of points
		y : Iterable
			The Y-coordinates of points

		Returns
		-------
		None
		"""
		for X, Y in zip(x, y):
			if isinstance(X, (QDateTime, datetime)):
				if isinstance(X, datetime):
					X = QDateTime(X)
				series.append(X.toMSecsSinceEpoch(), float(Y))
			elif isinstance(Y, (QDateTime, datetime)):
				if isinstance(Y, datetime):
					Y = QDateTime(Y)
				series.append(float(X), Y.toMSecsSinceEpoch())
			else:
				series.append(float(X), float(Y))

	def _setup_bar_series(self, bar_series, sets: dict, xlabels: list = None, percent: bool = False, legend: bool = True):
		"""Setup the bar set and axis for a bar or bar percent series.

		Parameters
		---------
		bar_series : QAbstractBarSeries
			The bar series to setup the bar sets and axis.
		sets : Dict[label, values], format: {"label for the set": [3, 2, 1,...]}
			The sets to display in this bar series
		OPTIONAL[xlabels] : List[str]
			The labels to use for X axis.
			Default: range(size_of_sets_values)
		OPTIONAL[percent] : bool
			Specify if the bar series is a percent bar series.
			Default: False 
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		# min and max value to define the Y axis after
		min_value = None
		max_value = None

		# Create bar set
		for label, values in sets.items():
			bar_set = QtCharts.QBarSet(label)
			bar_set.append(values)
			bar_series.append(bar_set)
			if min_value is None or min_value > min(values):
				min_value = min(values)
			if max_value is None or max_value < max(values):
				max_value = max(values)

		# X axis
		x_axis = QtCharts.QBarCategoryAxis()
		if xlabels is not None:
			x_axis.append(xlabels)
		else:
			x_axis.append[list(range(len(sets.values()[0])))]
		self.chart.addAxis(x_axis, Qt.AlignBottom)

		# Y Axis
		if not percent and min_value == max_value:
			max_value *= 0.2
		elif percent:
			min_value, max_value = 0, 100
		y_axis = self._create_y_axis((min_value, max_value), y_axis_align=Qt.AlignLeft)

		bar_series.attachAxis(x_axis)
		bar_series.attachAxis(y_axis)

		self.chart.legend().setVisible(legend)

	def add_line_series(self, serie_name: str, x: list, y: list,
		datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm", legend: bool = True):
		"""Add a line series to  the chart with x and y data.

		Parameters
		---------
		serie_name : str
			The series name.
		x : Iterable
			Data for X axis
		y : Iterable
			Data for Y axis
		OPTIONAL[datetime_axis] : bool
			If True, the X axis is a QDatetimeAxis else a QValueAxis
			Default: False
		OPTIONAL[datetime_fmt] : str
			If datetime_axis is True, specify the datetime format.
			Default: "yyyy-MM-dd h:mm"
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		line_series = QtCharts.QLineSeries(name=serie_name)
		self._add_points_data(line_series, x, y)
		self.add_series(line_series)
		self._setup_axis(line_series, x, y, datetime_axis=datetime_axis, datetime_fmt=datetime_fmt, legend=legend)
		

	def add_bar_series(self, serie_name: str, sets: dict, xlabels: list = None, legend: bool = True):
		"""Add a bar series to the chart with the sets data.

		Parameters
		---------
		serie_name : str
			The series name.
		sets : Dict[label, values], format: {"label for the set": [3, 2, 1,...]}
			The sets to display in this bar series
		OPTIONAL[xlabels] : List[str]
			The labels to use for X axis.
			Default: range(size_of_sets_values)
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		bar_series = QtCharts.QBarSeries(name=serie_name)
		self.add_series(bar_series)
		self._setup_bar_series(bar_series, sets, xlabels, percent=True, legend=legend)

	def add_barPercent_series(self, serie_name: str, data: dict, categories: list, legend: bool = True):
		"""Setup the bar set and axis for a bar or bar percent series.

		Parameters
		---------
		serie_name : str
			The series name.
		data : Dict[label, values], format: {"label for the set": [3, 2, 1,...]}
			The sets to display in this bar series
		categories : List[str]
			The labels to use for X axis.
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		bar_series = QtCharts.QPercentBarSeries(name=serie_name)
		self.add_series(bar_series)
		self._setup_bar_series(bar_series, data, categories, legend)

	def add_pie_series(self, serie_name: str, data: dict, legend: bool = True):
		"""Add a pie series to  the chart with data

		Parameters
		---------
		serie_name : str
			The series name.
		data : Dict[label, value], format: {"label1": 3, "label2": 6}
			Data for pie series
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		pie_series = QtCharts.QPieSeries(name=serie_name)
		for label, value in data.items():
			pie_series.append(label, value)
		self.add_series(pie_series)
		self.chart.legend().setVisible(legend)

	def add_scatter_series(self, serie_name: str, x: list = [], y: list = [], marker=QtCharts.QScatterSeries.MarkerShapeCircle,
		datetime_axis: bool = False, datetime_fmt: str = "yyyy-MM-dd h:mm", size: float = 10., legend: bool = True):
		"""Add a scatter series to  the chart with x and y data.

		Parameters
		---------
		serie_name : str
			The series name.
		x : Iterable
			Data for X axis
		y : Iterable
			Data for Y axis
		OPTIONAL[marker] : QScatterSeries.MarkerShape
			The shape of markers to use
			Default: QScatterSeries.MarkerShapeCircle
		OPTIONAL[datetime_axis] : bool
			If True, the X axis is a QDatetimeAxis else a QValueAxis
			Default: False
		OPTIONAL[datetime_fmt] : str
			If datetime_axis is True, specify the datetime format.
			Default: "yyyy-MM-dd h:mm"
		OPTIONAL[size] : float
			The size of markers
			Default: 10.
		OPTIONAL[legend] : bool
			Specify if the legend must be visible.
			Default: True

		Returns
		-------
		None
		"""
		scatter_series = QtCharts.QScatterSeries(name=serie_name)
		scatter_series.setMarkerSize(size)
		scatter_series.setMarkerShape(marker)
		self._add_points_data(scatter_series, x, y)
		self.add_series(scatter_series)
		self._setup_axis(scatter_series, x, y, datetime_axis=datetime_axis, datetime_fmt=datetime_fmt, legend=legend)

	def clear_chart(self):
		"""Clear all the chart"""
		self.chart.removeAllSeries()
		for axis in self.chart.axes():
			self.chart.removeAxis(axis)

	def save(self, path: str) -> str:
		"""Save the current chart in the specified path.

		Parameters
		---------
		path : str
			The path where saves the graph

		Returns
		-------
		path : str
			The path where the graph is saved
		"""
		im = self.chartView.grab()
		im.save(path)
		return path

	@Slot()
	def on_toolButton_clicked(self):
		"""Slot called when the signal 'clicked' of toolbutton is emited."""
		if self.chartView.isHidden():
			self.resize(self.width(), self._old_height)
			self.toolButton.setArrowType(Qt.DownArrow)
			self.chartView.show()
			self.retracted.emit(False)

		else:
			self._old_height = self.height()
			self.resize(self.width(), 40)
			self.toolButton.setArrowType(Qt.RightArrow)
			self.chartView.hide()
			self.retracted.emit(True)


if __name__ == "__main__":
	import sys
	from PySide6.QtWidgets import QApplication

	app = QApplication(sys.argv)
	line_graph = GraphicWidget()
	scatter_graph = GraphicWidget()
	bar_graph = GraphicWidget()
	barPercent_graph = GraphicWidget()
	pie_graph = GraphicWidget()

	# scatter
	scatter_graph.set_title("Scatter chart example")
	scatter_graph.add_scatter_series('scatter_carré', x=list(range(20)), y=[i**2 for i in range(20)])
	scatter_graph.add_scatter_series('scatter_cube', x=list(range(20)), y=[i**3 for i in range(20)])

	# pie
	pie_graph.set_title("Pie chart example")
	sets_pie = {"Choix 1": 3, "Choix 2": 2, "Choix 3": 7, "Choix 4": 5}
	pie_graph.add_pie_series("pie_test", sets_pie)

	# percent bar
	barPercent_graph.set_title("Percent bar chart example")
	sets_barPercent = {'Individu 1': [3, 6, 2, 8], "Individu 2": [6, 10, 1, 2], "Individu 3": [3, 5, 6, 4]}
	barPercent_graph.add_barPercent_series("bar percent test", sets_barPercent, ['jan', 'fev', 'mars', 'avril'])

	# bar
	bar_graph.set_title("Bar chart example")
	sets_bar = {"Individu A": [2, 2, 2, 2], "Individu B": [0, 3, 7, 14], "Individu C": [9, 12, 3, 1]}
	bar_graph.add_bar_series('series 1', sets=sets_bar, xlabels=['choix 1', 'choix 2', 'choix 3', 'choix 4'])

	# line
	line_graph.set_title("Line chart example")
	import numpy as np
	from PySide6.QtCore import QDateTime, QDate, QTime
	x = np.array([QDateTime(QDate(2021, j, i), QTime(12, 0)).toMSecsSinceEpoch() for j in range(3, 6) for i in range(1, 31)])
	line_graph.add_line_series('series 1', x=x, y=[i**2 + 100 for i in range(90)], datetime_axis=True)
	
	line_graph.show()
	scatter_graph.show()
	bar_graph.show()
	barPercent_graph.show()
	pie_graph.show()

	rc = app.exec()
	sys.exit(rc)

