import logging

from PySide2.QtWidgets import QPlainTextEdit

from QtHandlers import QtStreamHandler

class PlainTextEditHandler(QPlainTextEdit):
	def __init__(self, parent=None, handler: QtStreamHandler = None):
		QPlainTextEdit.__init__(self, parent)
		self.setReadOnly(True)
		self.handler = handler
		if self.handler is not None:
			self.handler.setPlainTextEdit(self)

	def setHandler(self, handler: QtStreamHandler):
		if isinstance(handler, QtStreamHandler):
			self.handler = handler
			self.handler.setPlainTextEdit(self)
		else:
			raise ValueError(f"handler must be a instance of 'QtStreamHandler' not {type(handler)}")