"""
A Toggle Button animated. This code was created by learnpyqt
Source: learnpyqt - https://www.learnpyqt.com/
"""

from PyQt5.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty)

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter


class ToggleButtonAnimated(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE",
        animated: bool = True
        ):
        QCheckBox.__init__(self, parent)

        self._animated = animated
        self._bar_color = QColor(bar_color)
        self._bar_checked_color =QColor(checked_color).lighter()

        self._handle_color = QColor(handle_color)
        self._handle_checked_color = QColor(checked_color)

        self._pulse_unchecked_color = QColor(pulse_unchecked_color)
        self._pulse_checked_color = QColor(pulse_checked_color)

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handlePosition", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulseRadius", self)
        self.pulse_anim.setDuration(400)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(25)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        if self._animated:
            self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def draw_bar(self, painter: QPainter):
        painter.save()
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

         # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.animation.state() == QPropertyAnimation.Running:
            painter.setBrush(self.pulseCheckedColor if self.isChecked() else self.pulseUncheckedColor)
            painter.drawEllipse(QPointF(xPos, barRect.center().y()), self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            painter.setBrush(self.barCheckedColor)
            painter.drawRoundedRect(barRect, rounding, rounding)

        else:
            painter.setBrush(self.barColor)
            painter.drawRoundedRect(barRect, rounding, rounding)
            painter.setPen(self._light_grey_pen)

        painter.restore()
        return barRect

    def draw_handle(self, painter, barRect):
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position
        painter.save()
        painter.setBrush(self.handleCheckedColor if self.isChecked() else self.handleColor)
        painter.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)
        painter.restore()

    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._transparent_pen)

        barRect = self.draw_bar(painter)
        self.draw_handle(painter, barRect)

        painter.end()

    @pyqtProperty(float)
    def handlePosition(self):
        return self._handle_position

    @handlePosition.setter
    def handlePosition(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self.update()
        self._handle_position = pos

    @pyqtProperty(float)
    def pulseRadius(self):
        return self._pulse_radius

    @pulseRadius.setter
    def pulseRadius(self, pos):
        self.update()
        self._pulse_radius = pos

    @pyqtProperty(QColor)
    def barColor(self):
        return self._bar_color

    @barColor.setter
    def barColor(self, color: QColor):
        self._bar_color = QColor(color)

    @pyqtProperty(QColor)
    def barCheckedColor(self):
        return self._bar_checked_color

    @barCheckedColor.setter
    def barCheckedColor(self, color: QColor):
        self._bar_checked_color = QColor(color)

    @pyqtProperty(QColor)
    def handleColor(self):
        return self._handle_color

    @handleColor.setter
    def handleColor(self, color: QColor):
        self._handle_color = QColor(color)

    @pyqtProperty(QColor)
    def handleCheckedColor(self):
        return self._handle_checked_color

    @handleCheckedColor.setter
    def handleCheckedColor(self, color: QColor):
        self._handle_checked_color = QColor(color)

    @pyqtProperty(QColor)
    def pulseUncheckedColor(self):
        return self._pulse_unchecked_color

    @pulseUncheckedColor.setter
    def pulseUncheckedColor(self, color: QColor):
        self._pulse_unchecked_color = QColor(color)

    @pyqtProperty(QColor)
    def pulseCheckedColor(self):
        return self._pulse_checked_color

    @pulseCheckedColor.setter
    def pulseCheckedColor(self, color: QColor):
        self._pulse_checked_color = QColor(color)

    @pyqtProperty(bool)
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, value: bool):
        if value and not self._animated:
            self.animations_group.addAnimation(self.pulse_anim)
        elif not value and self._animated:
            self.animations_group.removeAnimation(self.pulse_anim)
        self._animated = value


if __name__ == '__main__':
    import sys
    import time
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton
    from PyQt5.QtCore import Qt

    class Widget(QWidget):
        def __init__(self):
            super().__init__()
            self.button = ToggleButtonAnimated(self, animated=True)
            layout = QVBoxLayout()
            layout.addWidget(self.button)
            self.setLayout(layout)


    app = QApplication(sys.argv)
    w = Widget()
    w.setGeometry(100, 100, 600, 400)
    w.show()
    sys.exit(app.exec_())
