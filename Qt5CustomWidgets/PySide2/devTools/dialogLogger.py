from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from QtHandlers import QtStreamHandler
from plainTextEditHandler import PlainTextEditHandler


class DialogLogger(QDialog):
	def __init__(self, handler: QtStreamHandler, parent=None):
		QDialog.__init__(self, parent)
		self.plainTextEditHandler = PlainTextEditHandler(self, handler)
		self.buttons_box = QDialogButtonBox(QDialogButtonBox.Close, self)
		layout = QVBoxLayout()
		layout.addWidget(self.plainTextEditHandler)
		layout.addWidget(self.buttons_box)
		self.setLayout(layout)
		self.resize(600, 320)

		self.buttons_box.accepted.connect(self.accept)
		self.buttons_box.rejected.connect(self.reject)

	def closeEvent(self, e):
		self.plainTextEditHandler.handler.removePlainTextEdit()
		QDialog.closeEvent(self, e)


if __name__ == "__main__":
	import sys
	from PySide2.QtWidgets import QApplication
	app = QApplication(sys.argv)
	handler = QtStreamHandler()
	w = DialogLogger(handler)
	w.show()
	sys.exit(app.exec_())