from PyQt5 import QtWidgets, QtCore, QtGui

class RoundedLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(RoundedLabel, self).__init__(parent)
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap_original = pixmap
        self.update_pixmap()

    def resizeEvent(self, event):
        self.update_pixmap()
        super(RoundedLabel, self).resizeEvent(event)

    def update_pixmap(self):
        if self.pixmap_original:
            self.pixmap = self.pixmap_original.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.update()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QtGui.QPainter(self)
            painter.setRenderHints(QtGui.QPainter.Antialiasing, True)
            path = QtGui.QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, self.pixmap)
