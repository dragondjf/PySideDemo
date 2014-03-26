#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
from dbdata import getDataByID

class DisplayerManger(QtCore.QObject):

    def __init__(self, parent=None):
        super(DisplayerManger, self).__init__(parent)

    @classmethod
    def switchScreen(cls, viewID, dbID=''):
    	from viewmanger import views
        stLayout = views['mainwindow'].layout()
        if isinstance(stLayout, QtGui.QStackedLayout):
            if dbID:
                data = getDataByID(dbID)
                controller = getattr(views[viewID], 'controller')
                controller.updateByID(viewID, data)
                stLayout.setCurrentWidget(views[viewID])
            else:
                stLayout.setCurrentWidget(views[viewID])
