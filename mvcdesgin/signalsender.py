#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore


class SingleManager(QtCore.QObject):

    methodsin = QtCore.Signal(str)

    def __init__(self):
        super(SingleManager, self).__init__()

singleManager = SingleManager()


class SignalThread(QtCore.QThread):

    def __init__(self):
        super(SignalThread, self).__init__()
        self.timer = QtCore.QTimer()
        self.timer.moveToThread(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sendSignal)

    def run(self):
        self.timer.start()
        self.exec_()

    def sendSignal(self):
        singleManager.methodsin.emit('alert')
