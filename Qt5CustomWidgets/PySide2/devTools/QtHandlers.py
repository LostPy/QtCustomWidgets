from PySide2.QtWidgets import QPlainTextEdit
import logging


class QtStreamHandler(logging.Handler):
	def __init__(self, plain_text_edit: QPlainTextEdit = None):
		logging.Handler.__init__(self)

		self.plainText = plain_text_edit

	def setPlainTextEdit(self, plain_text_edit: QPlainTextEdit):
		if isinstance(plain_text_edit, QPlainTextEdit):
			self.plainText = plain_text_edit
		else:
			raise ValueError(f"plain_text_edit must be a instance of QtWidgets.QPlainTextEdit not '{type(plain_text_edit)}'")

	def removePlainTextEdit(self):
		self.plainText = None

	def emit(self, record):
		msg = self.format(record)
		if self.plainText is not None:
			self.plainText.appendPlainText(msg)

