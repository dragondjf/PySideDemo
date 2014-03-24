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




ScreenType = ['app', 'mfd', 'command', 'submenu']
ScreenSize = ['3', '4', '5', '8']



class ViewManger(object):
    """docstring for Application"""
    
    screenType = []
    screenSize = []
    views = []
    groups = {}
    currentSize = 3
    currentType = 'app'

    def __init__(self, arg):
        super(Application, self).__init__()
        self.arg = arg
    
    @classmethod
    def register(cls, view):
        if screenSize not in cls.screenSize:
            cls.screenSize.append(view.screenSize)
        if screenType not in cls.screenType:
            cls.screenType.append(view.screenType)
        if view not in cls.views:
            cls.views.append(view)
        cls.groups.update({(screenSize, screenType): view})

    @classmethod
    def getView(cls, currentSize, currentType):
        key = (currentSize, currentType)
        if key in cls.groups:
            return cls.groups[key]


class BaseModel(object):

    """docstring for BaseModel"""

    views = []

    def __init__(self, arg):
        super(BaseModel, self).__init__()
        self.arg = arg

    def registerView(self, view):
        self.views.append(view)
        ViewManger.register(view)

    def notify(self):
        self.prepareNotify()
        self.currentView.updateUI(data)
        self.finishNotify()

    def prepareNotify(self):
        pass

    def finishNotify(self):
        pass

    @property
    def currentView(self):
        key = (ViewManger.currentSize, view.currentType)
        self._currentView = ViewManger.getView()
        return self._currentView


class BaseView(object):

    """docstring for Screen"""

    screenType = ''
    screenSize = ''

    def __init__(self, parent=None):
        super(BaseView, self).__init__(parent)
        self.parent = parent

    def updateUI(self, data):
        pass

    def clearUI(self):
        pass


class BaseController(object):

    """docstring for BaseController"""

    def __init__(self, model=None):
        super(BaseController, self).__init__()
        self.model = model

    def register(self, view=None):
        if model and view:
            self.model.registerView(view)

    def update(self):
        self.model.notify()


class showModel(BaseModel):

    t = "123"


class Label1(QtGui.QLabel, BaseView):

    def __init__(self, model, parent=None):
        BaseView.__init__()
        super(Label1, self).__init__(parent)

    def initUI(self):
        pass

    def updateUI(self, data):
        self.setText(data)


class Label2(QtGui.QLabel, BaseView):

    def __init__(self, model, parent=None):
        BaseView.__init__()
        super(Label2, self).__init__(parent)

    def initUI(self):
        pass

    def updateUI(self):
        self.setText(data)


class Label3(QtGui.QLabel, BaseView):

    def __init__(self, model, parent=None):
        BaseView.__init__()
        super(Label3, self).__init__(parent)

    def initUI(self):
        pass

    def updateUI(self):
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

        showModel()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

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
