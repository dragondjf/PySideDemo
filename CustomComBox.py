#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore


class CenterWindow(QtGui.QFrame):

    style = '''
        QFrame#CenterWindow{
            background-color: lightgray;
        }
        QComboBox{
            color:white;
            font-size: 15px;
            font-family: "Verdana";
            background-color: rgb(5, 9, 21);
        }

        QComboBox:on{
            background-color: rgb(5, 9, 21);
        }

        QComboBox::drop-down :on{
            background-color: rgb(5, 9, 21);
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
        }


        QComboBox QAbstractItemView {
            border: none;
            color:white;
            font-size: 15px;
            font-family: "Verdana";
         }

        QComboBox QAbstractItemView {
            color:white;
            font-size: 15px;
         }

        QComboBox QAbstractItemView::item{
            height: 25px;
            color:white;
            font-size: 15px;
         }

        QComboBox QAbstractItemView::item:selected{
            background-color: rgb(63, 147, 168);
        }

        QComboBox QAbstractItemView::item:hover{
            background-color: rgb(69, 187, 217);
        }

        QListView {
     show-decoration-selected: 1; /* make the selection span the entire width of the view */
 }

 QListView::item:alternate {
     background: #EEEEEE;
 }

 QListView::item:selected {
     border: 1px solid #6a6ea9;
 }

 QListView::item:selected:!active {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #ABAFE5, stop: 1 #8588B2);
 }

 QListView::item:selected:active {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #6a6ea9, stop: 1 #888dd9);
 }

 QListView::item:hover {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #FAFBFE, stop: 1 #DCDEF1);
 }
    '''

    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setObjectName("CenterWindow")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))  # 设置程序图标
        self.setFixedSize(800, 500)


class ListItemWidget(QtGui.QWidget):

    style = '''

        QPushButton#downButton{
            background-color: green;
        }

        QPushButton#downButton:pressed {
            background-color: red;
        }

        QLabel{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: red;
            border: none;
        }
        QLabel:hover{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: green;
            border: none;
        }

        QLabel#currentText{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: red;
            border: none;
        }
    '''

    def __init__(self, parent=None):
        super(ListItemWidget, self).__init__(parent)
        self.initUI()
        self.setStyleSheet(self.style)

    def initUI(self):
        self.label = QtGui.QLabel('1212121212')
        self.label.setObjectName('currentText')
        self.downButton = QtGui.QPushButton('^')
        self.downButton.setObjectName('downButton')
        self.listScrollArea = QtGui.QScrollArea()
        self.listScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.initSize()
        self.listwidget = QtGui.QWidget()
        listlayout = QtGui.QVBoxLayout()
        for i in xrange(10):
            route = "Route%d" % i
            itemWidget = QtGui.QLabel(route)
            listlayout.addWidget(itemWidget)
        listlayout.setContentsMargins(0, 0, 0, 0)
        listlayout.setSpacing(0)
        self.listwidget.setLayout(listlayout)
        self.listScrollArea.setWidget(self.listwidget)

        self.listScrollArea.hide()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.label, 0, 0)
        mainLayout.addWidget(self.downButton, 0, 1)
        mainLayout.addWidget(self.listScrollArea, 1, 0, 1, 2)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.downButton.clicked.connect(self.showListWidget)

    def initSize(self):
        self.setFixedSize(ItemWidget.width + 20, 200)
        self.downButton.setFixedWidth(40)
        self.label.setFixedWidth(self.width() - self.downButton.width())
        self.listScrollArea.setFixedHeight(80)

    def showListWidget(self):
        self.listScrollArea.setVisible(not self.listScrollArea.isVisible())


class ListItem(QtGui.QPushButton):
    """docstring for ListItem"""
    style = '''
        QPushButton{
            background-color: transparent;
        }
        QPushButton:hover {
            background-color: red;
        }
        QPushButton:pressed {
            background-color: transparent;
        }
    '''
    width = 100
    height = 40

    def __init__(self, text, parent=None):
        super(ListItem, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet(self.style)
        self.setText(text)

        self.deleteButton = QtGui.QPushButton(self)
        self.deleteButton.setFixedSize(20, 20)
        self.deleteButton.move(75, 10)

        self.clicked.connect(self.changeBgColor)

    def changeBgColor(self):
        self.setStyleSheet("QPushButton{background-color: green;}")


class DropDownArea(QtGui.QScrollArea):
    """docstring for DropDownArea"""
    def __init__(self, parent=None):
        super(DropDownArea, self).__init__(parent)
        self.parent = parent
        self.initUI()
        self.setFixedSize(300, 200)

    def initUI(self):
        self.listwidget = QtGui.QWidget()
        listlayout = QtGui.QVBoxLayout()
        for i in xrange(10):
            route = "Route%d" % i
            itemWidget = ListItem(route)
            listlayout.addWidget(itemWidget)
        listlayout.setContentsMargins(0, 0, 0, 0)
        listlayout.setSpacing(0)
        self.listwidget.setLayout(listlayout)
        self.setWidget(self.listwidget)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = DropDownArea()
    main.show()
    sys.exit(app.exec_())
