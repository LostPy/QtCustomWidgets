

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from ui_test import Ui_Form


class Test(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButtonAdd_clicked(self):
        self.ProgressBar.increaseValue(5)

    @pyqtSlot()
    def on_pushButtonRemove_clicked(self):
        self.ProgressBar.discreaseValue(5)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Test()
    w.show()
    sys.exit(app.exec_())