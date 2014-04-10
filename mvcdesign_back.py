#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore
import functools
import random
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

class SingleManager(QtCore.QObject):

    methodsin = QtCore.Signal(str)

    def __init__(self):
        super(SingleManager, self).__init__()

singleManager = SingleManager()

class SignalThread(QtCore.QThread):

    def __init__(self):
        super(SignalThread, self).__init__()
        self.timer = QtCore.QTimer()
        self.timer.moveToThread(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sendSignal)

    def run(self):
        self.timer.start()
        self.exec_()

    def sendSignal(self):
        singleManager.methodsin.emit('alert')


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



def getDataByID(dbID):
    data = {
        'apps': '11111',
        'mfd': '222222',
        'command': '3333333',
        'subMenu': '4444444',
    }
    return data[dbID]


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
        controller = controllers[routes[signalID]['controllerID']]
        controller.handleData(data + signalID)


class DisplayerManger(QtCore.QObject):

    def __init__(self, parent=None):
        super(DisplayerManger, self).__init__(parent)

    @classmethod
    def switchScreen(cls, viewID, dbID=''):
        stLayout = views['mainwindow'].layout()
        if isinstance(stLayout, QtGui.QStackedLayout):
            if dbID:
                data = getDataByID(dbID)
                controller = getattr(views[viewID], 'controller')
                controller.updateByID(viewID, data)
                stLayout.setCurrentWidget(views[viewID])
            else:
                stLayout.setCurrentWidget(views[viewID])


# class BaseModel(object):

#     'docstring for BaseModel'

#     views = []

#     def __init__(self):
#         super(BaseModel, self).__init__()

#     def registerView(self, view):
#         self.views.append(view)

#     def notify(self, data):
#         self.prepareNotify()
#         for view in self.views:
#             view.updateUI(data)
#         self.finishNotify()

#     def prepareNotify(self):
#         pass

#     def finishNotify(self):
#         pass


class BaseView(object):

    '''docstring for Screen'''

    viewID = 'BaseView'
    controller = None

    def updateUI(self, data):
        pass

    def clearUI(self):
        pass


class BaseController(object):

    '''docstring for BaseController'''

    def __init__(self):
        self.views = {}

    def registerView(self, viewID=None):
        if viewID:
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


# class showModel(BaseModel):

#     t = '123'

class AppsController(QtCore.QObject, BaseController):

    controllerID = 'apps'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(AppsController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)


AppsController()


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


class SubMenuController(QtCore.QObject, BaseController):

    controllerID = 'subMenu'

    @collectControllers
    def __init__(self, parent=None):
        BaseController.__init__(self)
        super(SubMenuController, self).__init__(parent)

    def handleData(self, data):
        self.update(data)


SubMenuController()



class AppsDisplayer_3(QtGui.QLabel, BaseView):

    style = '''
        background-color: red;
        font-size: 40px;
        color: white;
    '''

    viewID = 'appsDisplayer_3'

    @collectViews
    def __init__(self, parent=None):
        super(AppsDisplayer_3, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data)

class AppsDisplayer_4(QtGui.QLabel, BaseView):

    style = '''
        background-color: lightred;
        font-size: 40px;
        color: white;
    '''

    viewID = 'appsDisplayer_4'

    @collectViews
    def __init__(self, parent=None):
        super(AppsDisplayer_4, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data)


class MFDDisplayer(QtGui.QLabel, BaseView):

    style = '''
        background-color: green;
        font-size: 40px;
        color: white;
    '''

    viewID = 'mfdDisplayer'

    @collectViews
    def __init__(self, parent=None):
        super(MFDDisplayer, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data)


class CommandDisplayer(QtGui.QLabel, BaseView):

    style = '''
        background-color: blue;
        font-size: 40px;
        color: white;
    '''

    viewID = 'commandDisplayer'

    @collectViews
    def __init__(self, parent=None):
        super(CommandDisplayer, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

    def updateUI(self, data):
        self.setText(data)


class SubmenuDisplayer(QtGui.QLabel, BaseView):

    style = '''
        background-color: yellow;
        font-size: 40px;
        color: white;
    '''

    viewID = 'subMenuDisplayer'

    @collectViews
    def __init__(self, parent=None):
        super(SubmenuDisplayer, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)

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
    viewID = 'mainwindow'
    displayerSize = 4

    @collectViews
    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setObjectName('CenterWindow')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置程序图标
        self.setWindowIcon(
            QtGui.QIcon(os.sep.join([os.getcwd(), 'skin', 'images', 'icon.ico'])))
        self.setFixedSize(800, 500)
        self.setStyleSheet(self. style)\

        appsDisplayer_3 = AppsDisplayer_3()
        appsDisplayer_4 = AppsDisplayer_4()
        mfdDisplayer = MFDDisplayer()
        commandDisplayer = CommandDisplayer()
        subMenuDisplayer = SubmenuDisplayer()

        stLayout = QtGui.QStackedLayout(self)
        stLayout.addWidget(appsDisplayer_3)
        stLayout.addWidget(appsDisplayer_4)
        stLayout.addWidget(mfdDisplayer)
        stLayout.addWidget(commandDisplayer)
        stLayout.addWidget(subMenuDisplayer)
        self.setLayout(stLayout)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_F1:
            singleManager.methodsin.emit('addApp')
        elif event.key() == QtCore.Qt.Key_F2:
            singleManager.methodsin.emit('show')
        elif event.key() == QtCore.Qt.Key_F3:
            singleManager.methodsin.emit('addCommand')
        elif event.key() == QtCore.Qt.Key_F4:
            singleManager.methodsin.emit('addSubmenu')
        elif event.key() == QtCore.Qt.Key_Left:
            dbID = ['apps', 'mfd', 'command', 'subMenu'][random.randint(1, 4) - 1]
            if dbID == "apps":
                viewID = dbID + 'Displayer_' + str(self.displayerSize)
            else: 
                viewID = dbID + 'Displayer'
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Right:
            dbID = ['apps', 'mfd', 'command', 'subMenu'][random.randint(1, 4) - 1]
            if dbID == "apps":
                viewID = dbID + 'Displayer_' + str(self.displayerSize)
            else: 
                viewID = dbID + 'Displayer'
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Up:
            self.displayerSize = 3
            dbID = 'apps'
            viewID =dbID + 'Displayer_3'
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Down:
            self.displayerSize = 4
            dbID = 'apps'
            viewID =dbID + 'Displayer_4'
            DisplayerManger.switchScreen(viewID, dbID)


    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - \
                self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if hasattr(self, 'dragPosition'):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


routes = {
    'addApp': {
        'viewIDs': ['appsDisplayer_3', 'appsDisplayer_4'],
        'controllerID': 'apps',
        'dbID': 'apps'
    },
    'show': {
        'viewIDs': ['mfdDisplayer'],
        'controllerID': 'mfd',
        'dbID': 'mfd'
    },
    'addCommand': {
        'viewIDs': ['commandDisplayer'],
        'controllerID': 'command',
        'dbID': 'command'
    },
    'delCommand': {
        'viewIDs': ['commandDisplayer'],
        'controllerID': 'command',
        'dbID': 'command'
    },
    'addSubmenu': {
        'viewIDs': ['subMenuDisplayer'],
        'controllerID': 'subMenu',
        'dbID': 'subMenu'
    },
    'delsubMenu': {
        'viewIDs': ['subMenuDisplayer'],
        'controllerID': 'subMenu',
        'dbID': 'subMenu'
    },
}


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # s = SignalThread()
    # s.start()
    main = CenterWindow()
    viewManger = ViewManger()
    main.show()
    sys.exit(app.exec_())
