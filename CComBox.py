#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore


class ListItem(QtGui.QPushButton):
    """docstring for ListItem"""
    style = '''
        QPushButton#ListItem{
            background-color: rgb(40, 47, 63);
            color: white;
            font-family: "Verdana";
            font-size: 15px;
            padding:5px;
            border: none;
            text-align: center, left;
        }
        QPushButton#ListItem:hover {
            background-color: rgb(69, 187, 217);
        }
        
        QPushButton#ListItem:pressed {
            background-color: rgb(63, 147, 168);
        }

        QPushButton#ListItemclicked{
            background-color: rgb(63, 147, 168);
            color: white;
            font-family: "Verdana";
            font-size: 15px;
            padding:5px;
            border: none;
            text-align: center, left;
        }

        QPushButton#deleteButton{
            border-image: url(view/skin/PNG/gmapdrive/deleteup.png);
            background-color: transparent;
        }

        QPushButton#deleteButton:pressed {
            border-image: url(view/skin/PNG/gmapdrive/deletedown.png);
            background-color: transparent;
        }
    '''

    # clicked = QtCore.Signal()
    deleted = QtCore.Signal(object)

    h = 30

    def __init__(self, text, deleteflag=True, parent=None):
        super(ListItem, self).__init__(parent)
        self.setObjectName("ListItem")
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.parent = parent
        self.setText(text)
        if deleteflag:
            self.deleteButton = QtGui.QPushButton(self)
            self.deleteButton.setObjectName("deleteButton")
            self.deleteButton.hide()
            self.deleted.connect(self.parent.deleteItem)
            self.deleteButton.clicked.connect(self.deleteSelf)
            self.deleteButton.setFixedSize(20, 20)
        self.setFixedSize(self.parent.width(), self.h)
        self.setStyleSheet(self.style)
        self.installEventFilter(self)

        self.clicked.connect(self.parent.selected)

    def updateButtonPos(self):
        if hasattr(self, 'deleteButton'):
            deleteButton_pos_x = self.width() - self.deleteButton.width() - 5
            deleteButton_pos_y = (self.height() - self.deleteButton.height()) / 2
            self.deleteButton.move(deleteButton_pos_x - 5, deleteButton_pos_y)

    def deleteSelf(self):
        self.deleted.emit(self)

    def resizeEvent(self, event):
        self.updateButtonPos()
        super(ListItem, self).resizeEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            if hasattr(self, 'deleteButton'):
                self.deleteButton.show()
            return super(ListItem, self).eventFilter(obj, event)
        elif event.type() == QtCore.QEvent.HoverLeave:
            if hasattr(self, 'deleteButton'):
                self.deleteButton.hide()
            return super(ListItem, self).eventFilter(obj, event)
        else:
            return super(ListItem, self).eventFilter(obj, event)


class ListWidget(QtGui.QFrame):

    currentIndexChanged = QtCore.Signal(int)
    currentTextChanged = QtCore.Signal(str)
    acticved = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.parent = parent
        self.items = []
        self.itemWidgets = []
        self.currentIndex = 0
        self.initUI()

    def initUI(self):
        self.setFixedWidth(self.parent.width() - 20)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

    def selected(self):
        if self.itemWidgets.index(self.sender()) == 0:
            self.parent.hide()
        else:
            for itemWidget in self.itemWidgets:
                if itemWidget is self.sender():
                    itemWidget.setObjectName("ListItemclicked")
                else:
                    itemWidget.setObjectName("ListItem")
                itemWidget.setStyleSheet(itemWidget.style)
            self.acticved.emit(self.sender().text())
        self.currentIndex = self.itemWidgets.index(self.sender())
        self.currentIndexChanged.emit(self.currentIndex)

    def selectedbyIndex(self, index):
        self.itemWidgets[index].click()
        if index == 0:
            self.parent.hide()
        self.currentIndexChanged.emit(index)

    def addItemWidget(self, itemWidget):
        self.itemWidgets.append(itemWidget)
        self.layout().addWidget(itemWidget)
        self.currentIndex = len(self.itemWidgets) - 1
        self.selectedbyIndex(self.currentIndex)
        self.setFixedHeight(self.layout().count() * 30)
        self.updateScrollBar()

    def addItemWidgets(self, itemWidgets):
        for itemWidget in itemWidgets:
            self.addItemWidget(itemWidget)

    def addItem(self, item):
        itemWidget = ListItem(item, True, self)
        self.itemWidgets.append(itemWidget)
        self.layout().addWidget(itemWidget)
        self.currentIndex = len(self.itemWidgets) - 1
        self.selectedbyIndex(self.currentIndex)
        self.setFixedHeight(self.layout().count() * 30)

        self.updateScrollBar()

    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def deleteItem(self, item):
        index = self.itemWidgets.index(item)

        if index >= 1:
            self.currentIndex = index
        if index == len(self.itemWidgets) - 1:
            self.currentIndex = index - 1

        self.itemWidgets.remove(item)
        self.layout().removeWidget(item)
        self.selectedbyIndex(self.currentIndex)

        if len(self.itemWidgets) == 1:
            self.parent.parent.titleButton.setText("")
            self.currentIndex = None

        self.setFixedHeight(self.layout().count() * 30)
        self.updateScrollBar()

    def updateScrollBar(self):
        l = len(self.parent.listWidget.itemWidgets)
        if l <= 5:
            self.parent.setFixedSize(self.parent.width(), ListItem.h * l)
            self.parent.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        else:
            self.parent.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

            # vs = self.parent.verticalScrollBar()
            # vs.setMinimum(0)
            # vs.setMaximum(len(self.itemWidgets))
            # vs.setValue(self.currentIndex)
            # print self.currentIndex
        self.update()

class DropDownBox(QtGui.QScrollArea):

    style = '''
        QScrollArea{
            background-color: rgb(40, 47, 63);
        }
        
        QScrollBar:vertical {
            border: 1px solid #252A31;
            width: 10px;
            margin: 15px 0 15px 0;
            background: #5B677A;
        }
        QScrollBar::handle:vertical {
            background: #31394E;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical {
            background: #252A31;
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            background: #252A31;
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        /*QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            width: 3px;
            height: 3px;
            background: #31394E;
        }*/

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
    '''

    def __init__(self, parent=None):
        super(DropDownBox, self).__init__(parent)
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.initUI()
        self.installEventFilter(self)
        self.showflag = False

    def initUI(self):
        self.setFixedSize(140, 150)
        self.listWidget = ListWidget(self)
        self.setWidget(self.listWidget)
        self.setStyleSheet(self.style)
        # self.ensureWidgetVisible(self.listWidget, 0, 0)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if not self.parent.titleButton.geometry().contains(self.parent.mapFromGlobal(event.globalPos())):
                self.hide()
                self.showflag = True
            else:
                self.hide()
                self.showflag = False
            return super(DropDownBox, self).eventFilter(obj, event)
        else:
            return super(DropDownBox, self).eventFilter(obj, event)


class ComBox(QtGui.QFrame):

    style = '''
         QPushButton#titleButton{
            color:white;
            font-size: 15px;
            font-family: "Verdana";
            text-align: left;
            padding: 5px;
            background-image: url(View/skin/PNG/downarrow.png);
            background-position: center right;
            background-repeat: no-repeat;
            background-color: rgb(5, 9, 21);
        }
    '''

    def __init__(self, parent=None):
        super(ComBox, self).__init__(parent)
        self.count = 0
        self.initUI()

        self.currentIndexChanged = self.dropdownBox.listWidget.currentIndexChanged
        self.acticved = self.dropdownBox.listWidget.acticved
        self.acticved.connect(self.updateTitle)

    def initUI(self):
        self.titleButton = QtGui.QPushButton()
        self.titleButton.setObjectName("titleButton")
        self.titleButton.setFixedSize(140, 30)
        self.titleButton.clicked.connect(self.hideshow)
        self.titleButton.setStyleSheet(self.style)

        self.dropdownBox = DropDownBox(self)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.titleButton)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

    def hideshow(self):
        point  = self.rect().bottomLeft()
        global_point = self.mapToGlobal(point)
        self.dropdownBox.move(global_point)

        if self.count > 0:
            if self.dropdownBox.showflag:
                self.dropdownBox.setVisible(not self.dropdownBox.isVisible())
            else:
                self.dropdownBox.hide()
                self.dropdownBox.showflag = True
        else:
            self.dropdownBox.show()
        self.count += 1

    def addItemWidget(self, itemWidget):
        self.dropdownBox.listWidget.addItemWidget(itemWidget)

    def addItemWidgets(self, itemWidgets):
        self.dropdownBox.listWidget.addItemWidgets(itemWidgets)

    def addItem(self, item):
        self.dropdownBox.listWidget.addItem(item)

    def addItems(self, items):
        self.dropdownBox.listWidget.addItems(items)

    def deleteItem(self, item):
        self.dropdownBox.listWidget.deleteItem(item)

    def updateTitle(self, text):
        self.titleButton.setText(text)


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
        self.setWindowIcon(QtGui.QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))  # 设置程序图标
        self.setFixedSize(800, 500)
        
        self.ccbox = ComBox(self)
        self.ccbox.move(100, 60)

        self.ccbox.currentIndexChanged.connect(self.updateroutes)

        listitem = ListItem("New...", False, self.ccbox.dropdownBox.listWidget)
        self.ccbox.addItemWidget(listitem)
        self.ccbox.addItems(['route%d' % i for i in xrange(10)])


        QtGui.QLabel("54545454", self).move(200, 100)

        self.addButton = QtGui.QPushButton("add", self)
        self.addButton.clicked.connect(self.addroute)
        self.addButton.move(300, 100)


        self.routecomboBox = QtGui.QComboBox(self)
        self.routecomboBox.move(200, 300)
        for i in xrange(10):
            self.routecomboBox.addItem("route%d"% i)
        self.setStyleSheet(self. style)

    def addroute(self):
        import random
        self.ccbox.addItem('route%d' % random.randint(0, 100))

    def updateroutes(self, index):
        print 'route',index

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = CenterWindow()
    main.show()
    sys.exit(app.exec_())
