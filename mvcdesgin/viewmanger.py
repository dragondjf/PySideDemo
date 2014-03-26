#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore
import functools
import random
from signalsender import singleManager
from routes import routes
'''
原则：
1. 视图层每一个控件，仅仅包含UI元素及更新ui元素的接口,自定义事件接口
    + __init__
    + initUI()
    + updateUI()
    + clearUI()
    + event()
    + ...

2. 每一个控制器创建一个model, 每个model注册一个或多个view；
3. 控制器通知model改变状态， model通知当前视图更新数据


'''


views = {}
controllers = {}

def collectViews(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwars):
        fn(*args, **kwars)
        views.update({args[0].viewID: args[0]})
    return wrapper

def collectControllers(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwars):
        fn(*args, **kwars)
        controllers.update({args[0].controllerID: args[0]})
    return wrapper


class ViewManger(QtCore.QObject):

    def __init__(self, parent=None):
        super(ViewManger, self).__init__(parent)
        self.registerViews()
        singleManager.methodsin.connect(self.receiveSignal)

    def registerViews(self):
        for signalID in routes:
            controller = controllers[routes[signalID]['controllerID']]
            for viewID in routes[signalID]['viewIDs']:
                controller.registerView(viewID)
                setattr(views[viewID], 'controller', controller)

    @QtCore.Slot(str)
    def receiveSignal(self, signalID):
        dbID = routes[signalID]['dbID']
        data = getDataByID(dbID)
        controller = self.controllers[routes[signalID]['controllerID']]
        controller.handleData(data + signalID)
