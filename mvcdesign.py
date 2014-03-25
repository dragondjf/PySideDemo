#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore
import functools
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


def registerView(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwars):
        fn(*args, **kwars)
        views.update({args[0].viewID: args[0]})
    return wrapper


def switchScreen(viewID):
    stLayout = views['mainwindow'].layout()
    if isinstance(stLayout, QtGui.QStackedLayout):
        stLayout.setCurrentWidget(views[viewID])


def getDataByID(signalID):
    return signalID



class ViewManger(QObject):

    def __init__(self, parent=None):
        super(ViewManger, self).__init__(parent)

    @QtCore.Slot(str)
    def receiveSignal(self, signalID):
        request = getDataByID(signalID)
        # controller = get

class BaseModel(object):

    """docstring for BaseModel"""

    views = []

    def __init__(self):
        super(BaseModel, self).__init__()

    def registerView(self, view):
        self.views.append(view)

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

    viewID = ''
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

    viewID = "l1"
    viewSize = 1

    @registerView
    def __init__(self, parent=None):
        super(Label1, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data + self.viewID)
        # self.show()


class Label2(QtGui.QLabel, BaseView):

    viewID = "l2"
    viewSize = 2

    @registerView
    def __init__(self, parent=None):
        super(Label2, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data + self.viewID)


class Label3(QtGui.QLabel, BaseView):

    viewID = "l3"
    viewSize = 3

    @registerView
    def __init__(self, parent=None):
        super(Label3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedSize(100, 50)

    def updateUI(self, data):
        self.setText(data + self.viewID)


# l1 = Label1()
# l1.move(100, 100)
# l2 = Label2()
# l2.move(200, 100)
# l3 = Label3()
# l3.move(300, 100)


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
    viewID = "mainwindow"

    @registerView
    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setObjectName("CenterWindow")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置程序图标
        self.setWindowIcon(
            QtGui.QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))
        self.setFixedSize(800, 500)
        self.setStyleSheet(self. style)\

        # self.l1 = Label1(self)
        # self.l1.move(100, 100)
        # self.l2 = Label2(self)
        # self.l2.move(200, 100)
        # self.l3 = Label3(self)
        # self.l3.move(300, 100)
        l1 = Label1()
        l2 = Label2()
        l3 = Label3()
        stLayout = QtGui.QStackedLayout(self)
        stLayout.addWidget(l1)
        stLayout.addWidget(l2)
        stLayout.addWidget(l3)
        self.setLayout(stLayout)

        self.controller = showController()
        self.controller.registerView(l1)
        self.controller.registerView(l2)
        self.controller.registerView(l3)

        import random
        self.controller.update('--%d--'%random.randint(1, 10))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key_F1:
            import random
            switchScreen('l%d' % random.randint(1, 3))
            print views

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
