from PyQt5.QtWidgets import QLineEdit


class MyLineEdit(QLineEdit):
	def __init__(self, parent=None):
		super(MyLineEdit, self).__init__(parent)
		self.setStyleSheet("background-color: yellow;")
