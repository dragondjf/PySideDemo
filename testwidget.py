#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PySide import QtGui
from PySide import QtCore
from IconButton import IconButton
import math

def set_skin(QApplication, qssfile, style=''):
    qss = None
    with open(qssfile) as f:
        qss = ''.join(f.readlines()) + style
    QApplication.setStyleSheet(qss)


def setbg(widget, filename):
    '''
        设置背景颜色或者图片,平铺
    '''
    widget.setAutoFillBackground(True)
    palette = QtGui.QPalette()
    pixmap = QtGui.QPixmap(filename)
    pixmap = pixmap.scaled(widget.size())
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
    widget.setPalette(palette)


class CenterWindow(QtGui.QDialog):

    style = '''
        QDialog{
            background-color:#3b4351;
        }
        QLabel{
            color: white;
            font-size: 20px;
        }
        QLabel#titleLabel{
            color: white;
            font-size: 30px;
        }
    '''

    def __init__(self, texts=['1', '2'], parent=None):
        super(CenterWindow, self).__init__(parent)
        self.textLabels = texts
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setModal(False)
        self.resize(500, 200)
        self.timecount = 0
        self.initUI()

        self.timerclock = QtCore.QTimer()
        self.timerclock.setInterval(100)
        self.timerclock.timeout.connect(self.changetime)
        self.timerclock.start()

    def initUI(self):
        mainlayout = QtGui.QVBoxLayout()
        self.titleLabel = QtGui.QLabel("Voice Record")
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        mainlayout.addWidget(self.titleLabel)
        mainlayout.addStretch()

        for text in self.textLabels:
            i = self.textLabels.index(text)
            setattr(self, 'textLabel%d' % i, QtGui.QLabel(text))
            label = getattr(self, 'textLabel%d' % i)
            label.setAlignment(QtCore.Qt.AlignLeft)
            mainlayout.addWidget(label)

        self.retryButton = IconButton(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "retry_up.png"]), \
            os.sep.join([os.getcwd(), "View", 'skin', "PNG", "retry_down.png"]), "ok", self)
        self.okButton = IconButton(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "done_up.png"]), \
            os.sep.join([os.getcwd(), "View", 'skin', "PNG", "done_down.png"]), "ok", self)
        self.cancelButton = IconButton(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cancel_up.png"]), \
            os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cancel_down.png"]), "cancel", self)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.retryButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.lcd = QtGui.QLCDNumber()
        self.lcd.display(self.timecount)

        timeLayout = QtGui.QHBoxLayout()
        timeLayout.addWidget(self.slider)
        timeLayout.addWidget(self.lcd)
        mainlayout.addLayout(timeLayout)

        mainlayout.addStretch()
        mainlayout.addLayout(buttonLayout)
        mainlayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(mainlayout)
        self.setStyleSheet(self.style)

    def changetime(self):
        self.timecount += 1
        if bool(math.fmod(self.timecount, 10)):
            self.slider.setValue(self.timecount)
            self.lcd.display(float(self.timecount)/10)
        if self.timecount == 100:
            self.timerclock.stop()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    texts = [
        "Don't do shit",
        "Just Go On"
    ]
    main = CenterWindow(texts)
    main.show()
    sys.exit(app.exec_())
