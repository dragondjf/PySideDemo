import os
from PySide import QtGui
from PySide import QtCore


class IconButton(QtGui.QPushButton):

    style = '''
        QPushButton{
            background-color: rgb(59,67,81);
            border: None;
        }

        QPushButton:focus{
            padding: -1;
        }
    '''

    def __init__(self, up, down, id, parent=None):
        super(IconButton, self).__init__(parent)
        self.pixmap_up = QtGui.QPixmap(up)
        self.pixmap_down = QtGui.QPixmap(down)
        self.up = QtGui.QIcon(self.pixmap_up)
        self.down = QtGui.QIcon(self.pixmap_down)
        self.setObjectName(id)
        self.setIcon(self.up)

        self.setIconSize(self.pixmap_up.size())
        self.setFixedSize(self.pixmap_up.size())

        self.resize(self.pixmap_up.size())
        self.setStyleSheet(self.style)
        self.pressed.connect(self.actionPress)
        self.released.connect(self.actionRelease)

    def actionPress(self):
        self.setIcon(self.down)

    def actionRelease(self):
        self.setIcon(self.up)
