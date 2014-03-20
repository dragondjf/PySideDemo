#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore


class ListItem(QtGui.QLabel):
    """docstring for ListItem"""
    style_normal = '''
        QLabel{
            background-color: rgb(40, 47, 63);
            color: white;
            font-family: "Verdana";
            font-size: 15px;
            padding: 5px;
            border: none;
        }
        QLabel:hover {
            background-color: rgb(69, 187, 217);
        }
        QPushButton{
            border-image: url(view/skin/PNG/gmapdrive/deleteup.png);
            background-color: transparent;
        }

        QPushButton:pressed {
            border-image: url(view/skin/PNG/gmapdrive/deletedown.png);
            background-color: transparent;
        }
    '''

    style_clicked = '''
        QLabel{
            background-color: rgb(63, 147, 168);
            color: white;
            font-family: "Verdana";
            font-size: 15px;
            padding: 5px;
            border: none;
        }
        QLabel:hover {
            background-color: rgb(69, 187, 217);
        }
        QPushButton{
            border-image: url(view/skin/PNG/gmapdrive/deleteup.png);
            background-color: transparent;
        }

        QPushButton:pressed {
            border-image: url(view/skin/PNG/gmapdrive/deletedown.png);
            background-color: transparent;
        }
    '''
    hovered = QtCore.Signal()
    clicked = QtCore.Signal()
    deleted = QtCore.Signal()

    h = 30

    def __init__(self, item, text, deleteflag=True, parent=None):
        super(ListItem, self).__init__(parent)
        # self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.item = item
        self.parent = parent
        self.setText(text)
        if deleteflag:
            self.deleteButton = QtGui.QPushButton(self)
            self.deleteButton.hide()
            self.deleteButton.setFixedSize(20, 20)
        self.setFixedSize(self.parent.width() - 20, self.h)
        self.setStyleSheet(self.style_normal)
        self.installEventFilter(self)

    def updateButtonPos(self):
        if hasattr(self, 'deleteButton'):
            deleteButton_pos_x = self.width() - self.deleteButton.width() - 5
            deleteButton_pos_y = (self.height() - self.deleteButton.height()) / 2
            self.deleteButton.move(deleteButton_pos_x - 5, deleteButton_pos_y)


    def mousePressEvent(self, event):
        self.clicked.emit()

    def mouseDoubleClickEvent (self, event):
        self.clicked.emit()
        self.parent.hide()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseMove:
            return True
        else:
            return super(ListItem, self).eventFilter(obj, event)

    def resizeEvent(self, event):
        self.updateButtonPos()
        super(ListItem, self).resizeEvent(event)


class CustomListWidget(QtGui.QListWidget):

    style = '''
        QListWidget{
            background-color:rgb(40, 47, 63);
        }

        QListWidget::item {
            border:none
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

    currentIndexChanged = QtCore.Signal(int)
    currentTextChanged = QtCore.Signal(str)

    def __init__(self, items, parent=None):
        super(CustomListWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.parent = parent
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedSize(self.parent.width(), ListItem.h * 5 + 5)
        self.itemWidgets = []

        self.currentIndexChanged.connect(self.parent.updateCurrentIndex)
        self.currentTextChanged.connect(self.parent.updateCurrentText)

        self.initList(items)
        self.setGridSize(QtCore.QSize(self.width(), ListItem.h))
        self.currentIndex = 1

        self.setStyleSheet(self.style)
        self.installEventFilter(self)

        self.showflag = False

    def initList(self, items):
        listItem = QtGui.QListWidgetItem(self)
        itemWidget = ListItem(listItem, 'New...', False, self)
        itemWidget.clicked.connect(self.highlighted)
        self.setItemWidget(listItem, itemWidget)
        self.itemWidgets.append(itemWidget)
        for route in items:
            self.addItemWidget(route)
        self.itemWidgets[1].clicked.emit()
        self.verticalScrollBar().setValue(1)

    def highlighted(self):
        index = self.row(self.sender().item)
        for itemWidget in self.itemWidgets:
            if itemWidget is self.sender():
                itemWidget.setStyleSheet(self.sender().style_clicked)
                if hasattr(itemWidget, 'deleteButton'):
                    itemWidget.deleteButton.show()
            else:
                itemWidget.setStyleSheet(self.sender().style_normal)
                if hasattr(itemWidget, 'deleteButton'):
                    itemWidget.deleteButton.hide()
        if index == self.currentIndex:
            pass
        else:
            self.currentIndex = index
            self.currentIndexChanged.emit(index)
            self.currentTextChanged.emit(self.sender().text())

        if index == 0:
            self.hide()

    def deleteItem(self):
        index = self.row(self.sender().parent().item)
        self.parent.items.pop(index - 1)
        self.itemWidgets.pop(index)
        self.takeItem(index)
        if len(self.itemWidgets) <= 5:
            self.setFixedSize(self.width(), ListItem.h * len(self.itemWidgets))
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setFixedSize(self.parent.width(), ListItem.h * len(self.itemWidgets) + 5)
        else:
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        if index == 1:
            self.itemWidgets[-1].clicked.emit()
            self.scrollToBottom()
        else:
            self.itemWidgets[index - 1].clicked.emit()

        if len(self.itemWidgets) == 1:
            self.hide()

    def addItemWidget(self, route):
        listItem = QtGui.QListWidgetItem(self)
        itemWidget = ListItem(listItem, route, True, self)
        itemWidget.clicked.connect(self.highlighted)
        itemWidget.deleteButton.clicked.connect(self.deleteItem)
        self.setItemWidget(listItem, itemWidget)
        self.itemWidgets.append(itemWidget)
        if len(self.itemWidgets) <= 5:
            self.setFixedSize(self.width(), ListItem.h * len(self.itemWidgets))
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.setFixedSize(self.parent.width(), ListItem.h * len(self.itemWidgets) + 5)
        else:
            self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        itemWidget.clicked.emit()

        vs = self.verticalScrollBar()
        vs.setMinimum(0)
        vs.setMaximum(len(self.itemWidgets))
        vs.setValue(len(self.itemWidgets))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            return True
        elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if not self.parent.button.geometry().contains(self.parent.mapFromGlobal(event.globalPos())):
                self.hide()
                self.showflag = True
            else:
                self.hide()
                self.showflag = False
            return super(CustomListWidget, self).eventFilter(obj, event)
        else:
            return super(CustomListWidget, self).eventFilter(obj, event)


class CustomComBox(QtGui.QWidget):
    style = '''
        QWidget{
            background-color: lightgray;
        }

        QPushButton#dropdown{
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

    currentIndexChanged = QtCore.Signal(int)
    currentTextChanged = QtCore.Signal(str)

    def __init__(self, items, parent=None):
        super(CustomComBox, self).__init__(parent)
        self.items = items or []
        self.parent = parent
        self.initUI()
        self.installEventFilter(self)
        self.count = 0

    def initUI(self):
        self.setFixedSize(140, 30)
        ListItem.h = self.height()
        mainLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel()
        self.label.setObjectName("currenttext")
        self.button = QtGui.QPushButton()
        self.button.setObjectName("dropdown")
        self.button.setFixedSize(140, self.height())
        self.button.pressed.connect(self.hideshow)

        # mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.button)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)
        self.setStyleSheet(self.style)

        self.customListWidget = CustomListWidget(self.items, self)

    def hideshow(self):
        point  = self.rect().bottomLeft()
        global_point = self.mapToGlobal(point)
        self.customListWidget.move(global_point)

        if self.count > 0:
            if self.customListWidget.showflag:
                self.customListWidget.setVisible(not self.customListWidget.isVisible())
            else:
                self.customListWidget.hide()
                self.customListWidget.showflag = True
        else:
            self.customListWidget.show()
        self.count += 1

    def updateCurrentText(self, text):
        self.button.setText(text)
        self.currentTextChanged.emit(text)

    def updateCurrentIndex(self, index):
        self.currentIndexChanged.emit(index)

    def addItem(self, item):
        self.customListWidget.addItemWidget(item)
        self.items.append(item)





class CustomBox2(QtGui.QComboBox):

    def __init__(self, parent=None):
        super(CustomBox2, self).__init__(parent)
        self.installEventFilter(self)
        print self.children()

    def eventFilter(self, obj, event):
        print event.type()
        #     print event.propertyName()
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            print '+++++++++++++'
            return super(CustomBox2, self).eventFilter(obj, event)
        else:
            return super(CustomBox2, self).eventFilter(obj, event)


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
        
        items = ['route%d'%i for i in xrange(10)]
        self.titleComBox = CustomComBox(items, self)
        self.titleComBox.move(100, 60)

        QtGui.QLabel("54545454", self).move(100, 100)

        self.addButton = QtGui.QPushButton("add", self)
        self.addButton.clicked.connect(self.addroute)
        self.addButton.move(300, 100)


        self.routecomboBox = CustomBox2(self)
        self.routecomboBox.move(200, 300)
        for i in xrange(10):
            self.routecomboBox.addItem("route%d"% i)
        self.setStyleSheet(self. style)

    def addroute(self):
        import random
        self.titleComBox.addItem('route%d' % random.randint(0, 100))

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
