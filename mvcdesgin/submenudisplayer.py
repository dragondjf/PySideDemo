#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from viewmanger import collectViews, collectControllers
from basecontroller import BaseController

class SubmenuDisplayer3(QtGui.QLabel):

    style = '''
        background-color: yellow;
        font-size: 40px;
        color: white;
    '''

    viewID = 'subMenuDisplayer3'

    @collectViews
    def __init__(self, parent=None):
        super(SubmenuDisplayer3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**3**')


class SubmenuDisplayer4(QtGui.QLabel):

    style = '''
        background-color: yellow;
        font-size: 40px;
        color: white;
    '''

    viewID = 'subMenuDisplayer4'

    @collectViews
    def __init__(self, parent=None):
        super(SubmenuDisplayer4, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data + '**4**')


class SubMenuController(QtCore.QObject, BaseController):

    controllerID = 'subMenu'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(SubMenuController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)


SubMenuController()
