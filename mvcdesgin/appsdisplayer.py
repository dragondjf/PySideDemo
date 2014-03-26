#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from viewmanger import collectViews, collectControllers
from basecontroller import BaseController

class AppDisplayer3(QtGui.QLabel):

    style = '''
        background-color: red;
        font-size: 40px;
        color: white;
    '''

    viewID = 'appDisplayer3'

    @collectViews
    def __init__(self, parent=None):
        super(AppDisplayer3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**3**')


class AppDisplayer4(QtGui.QLabel):

    style = '''
        background-color: red;
        font-size: 40px;
        color: white;
    '''

    viewID = 'appDisplayer4'

    @collectViews
    def __init__(self, parent=None):
        super(AppDisplayer4, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**4**')


class AppController(QtCore.QObject, BaseController):

    controllerID = 'app'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(AppController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)


AppController()
