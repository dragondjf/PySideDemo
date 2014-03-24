#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore

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


viewType = ['app', 'mfd', 'command', 'submenu']
viewSize = ['3', '4', '5', '8']


class ViewManger(object):
    """docstring for Application"""

    viewTypes = []
    viewSizes = []
    views = []
    groups = {}
    currentSize = 3
    currentType = 'app'

    def __init__(self, arg):
        super(ViewManger, self).__init__()
        self.arg = arg

    @classmethod
    def register(cls, view):
        if view.viewSize not in cls.viewSizes:
            cls.viewSizes.append(view.viewSize)
        if view.viewType not in cls.viewTypes:
            cls.viewTypes.append(view.viewType)
        if view not in cls.views:
            cls.views.append(view)
        cls.groups.update({(view.viewSize, view.viewType): view})

    @classmethod
    def getView(cls, currentSize, currentType):
        key = (currentSize, currentType)
        if key in cls.groups:
            return cls.groups[key]


class BaseModel(object):

    """docstring for BaseModel"""

    views = []

    def __init__(self):
        super(BaseModel, self).__init__()

    def registerView(self, view):
        self.views.append(view)
        ViewManger.register(view)

    def notify(self, data):
        self.prepareNotify()
        for view in self.views:
            view.updateUI(data)
        self.finishNotify()

    def prepareNotify(self):
        pass

    def finishNotify(self):
        pass


class BaseView(object):

    """docstring for Screen"""

    viewType = ''
    viewSize = 0

    def updateUI(self, data):
        pass

    def clearUI(self):
        pass


class BaseController(object):

    """docstring for BaseController"""
    modelClass = BaseModel

    def registerModel(self, model=None):
        self.model = model or self.modelClass()

    def registerView(self, view=None):
        if view:
            self.model.registerView(view)

    def update(self, data):
        self.model.notify(data)


class showModel(BaseModel):

    t = "123"


class showController(QtCore.QObject, BaseController):

    modelClass = showModel

    def __init__(self, parent=None):
        super(showController, self).__init__(parent)
        self.registerModel()


class Label1(QtGui.QLabel, BaseView):

    viewType = "l1"
    viewSize = 1

    def __init__(self, parent=None):
        super(Label1, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data)
        self.show()


class Label2(QtGui.QLabel, BaseView):

    viewType = "l2"
    viewSize = 2

    def __init__(self, parent=None):
        super(Label2, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data)


class Label3(QtGui.QLabel, BaseView):

    viewType = "l3"
    viewSize = 3

    def __init__(self, parent=None):
        super(Label3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data)


class CenterWindow(QtGui.QFrame):

    style = '''
        QFrame#CenterWindow{
            background-color: lightgray;
        }
        QFrame#w1{
            background-color: green;
        }
        QFrame#w2{
            background-color: red;
        }
    '''

    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setObjectName("CenterWindow")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置程序图标
        self.setWindowIcon(
            QtGui.QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))
        self.setFixedSize(800, 500)
        self.setStyleSheet(self. style)\

        self.l1 = Label1(self)
        self.l1.move(100, 100)
        self.l2 = Label2(self)
        self.l2.move(200, 100)
        self.l3 = Label3(self)
        self.l3.move(300, 100)

        self.controller = showController()
        self.controller.registerView(self.l1)
        self.controller.registerView(self.l2)
        self.controller.registerView(self.l3)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key_F1:
            import random
            self.controller.update('--%d--'%random.randint(1,10))
            print ViewManger.groups

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - \
                self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = CenterWindow()
    main.show()
    sys.exit(app.exec_())
