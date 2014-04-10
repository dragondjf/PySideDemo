#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from viewmanger import collectViews, collectControllers
from basecontroller import BaseController

class CommandDisplayer3(QtGui.QLabel):

    style = '''
        background-color: blue;
        font-size: 40px;
        color: white;
    '''

    viewID = 'commandDisplayer3'

    @collectViews
    def __init__(self, parent=None):
        super(CommandDisplayer3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**3**')


class CommandDisplayer4(QtGui.QLabel):

    style = '''
        background-color: blue;
        font-size: 40px;
        color: white;
    '''

    viewID = 'commandDisplayer4'

    @collectViews
    def __init__(self, parent=None):
        super(CommandDisplayer4, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**4**')


class CommandController(QtCore.QObject, BaseController):

    controllerID = 'command'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(CommandController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)

    def addAlert(self, data):
        pass

    def addcommand(self, data):
        pass

    def addMenu(self, data):
        pass

CommandController()
