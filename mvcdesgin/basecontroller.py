#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseController(object):

    '''docstring for BaseController'''

    def __init__(self):
        self.views = {}

    def registerView(self, viewID=None):
        if viewID:
            from viewmanger import views
            self.views.update({viewID: views[viewID]})

    def handleData(data):
        pass

    def update(self, data):
        for viewID, view in self.views.iteritems():
            if view.isVisible():
                view.updateUI(data)

    def updateByID(self, viewID, data):
        if viewID in self.views:
            self.views[viewID].updateUI(data)
