#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from viewmanger import collectViews, collectControllers
from basecontroller import BaseController

class MFDDisplayer3(QtGui.QLabel):

    style = '''
        background-color: green;
        font-size: 40px;
        color: white;
    '''

    viewID = 'mfdDisplayer3'

    @collectViews
    def __init__(self, parent=None):
        super(MFDDisplayer3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**3**')

class MFDDisplayer4(QtGui.QLabel):

    style = '''
        background-color: green;
        font-size: 40px;
        color: white;
    '''

    viewID = 'mfdDisplayer4'

    @collectViews
    def __init__(self, parent=None):
        super(MFDDisplayer4, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**4**')


class MFDController(QtCore.QObject, BaseController):

    controllerID = 'mfd'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(MFDController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)

    def addAlert(self, data):
        pass

    def addcommand(self, data):
        pass

    def addMenu(self, data):
        pass


MFDController()