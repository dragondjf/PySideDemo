#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore
import functools
import random
from appsdisplayer import AppDisplayer3, AppDisplayer4
from mfddisplayer import MFDDisplayer3, MFDDisplayer4
from commanddisplayer import CommandDisplayer3, CommandDisplayer4
from submenudisplayer import SubmenuDisplayer3, SubmenuDisplayer4

from viewmanger import collectViews
from viewmanger import ViewManger
from displayermanger import DisplayerManger
from signalsender import singleManager


class Mainwindow(QtGui.QFrame):

    style = '''
        QFrame#Mainwindow{
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
        super(Mainwindow, self).__init__(parent)
        self.setObjectName('Mainwindow')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置程序图标
        self.setWindowIcon(
            QtGui.QIcon(os.sep.join([os.getcwd(), 'skin', 'images', 'icon.ico'])))
        self.setFixedSize(800, 500)
        self.setStyleSheet(self. style)\

        appDisplayer3 = AppDisplayer3()
        appDisplayer4 = AppDisplayer4()
        mfdDisplayer3 = MFDDisplayer3()
        mfdDisplayer4 = MFDDisplayer4()
        commandDisplayer3 = CommandDisplayer3()
        commandDisplayer4 = CommandDisplayer4()
        subMenuDisplayer3 = SubmenuDisplayer3()
        subMenuDisplayer4 = SubmenuDisplayer4()

        stLayout = QtGui.QStackedLayout(self)
        stLayout.addWidget(appDisplayer3)
        stLayout.addWidget(appDisplayer4)
        stLayout.addWidget(mfdDisplayer3)
        stLayout.addWidget(mfdDisplayer4)
        stLayout.addWidget(commandDisplayer3)
        stLayout.addWidget(commandDisplayer4)
        stLayout.addWidget(subMenuDisplayer3)
        stLayout.addWidget(subMenuDisplayer4)
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
            dbID = ['app', 'mfd', 'command', 'subMenu'][random.randint(1, 4) - 1]
            viewID = dbID + 'Displayer' + str(self.displayerSize)
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Right:
            dbID = ['app', 'mfd', 'command', 'subMenu'][random.randint(1, 4) - 1]
            viewID = dbID + 'Displayer' + str(self.displayerSize)
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Up:
            self.displayerSize = 3
            dbID = 'app'
            viewID =dbID + 'Displayer3'
            DisplayerManger.switchScreen(viewID, dbID)
        elif event.key() == QtCore.Qt.Key_Down:
            self.displayerSize = 4
            dbID = 'app'
            viewID =dbID + 'Displayer4'
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





if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # s = SignalThread()
    # s.start()
    main = Mainwindow()
    viewManger = ViewManger()
    main.show()
    sys.exit(app.exec_())
