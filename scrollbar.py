#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PySide import QtGui
from PySide import QtCore


class ScrollBar(QtGui.QTableWidget):

    style = '''
        /*border: 2px solid #485260;*/
        /*border: none;*/
        /*color: white;*/
        background-color: #5B677A;
        selection-color: #252a31;
        selection-background-color:#485260;
    '''

    def __init__(self, row, count=1, parent=None):
        super(ScrollBar, self).__init__(row, count, parent)
        self.setFixedSize(20, 250)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setAutoScroll(False)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setShowGrid(True)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.initUI()

    def initUI(self):
        self.setStyleSheet(self.style)
        for i in xrange(self.rowCount()):
            self.setRowHeight(i, 250 / self.rowCount())
        self.multiselect([2, 3, 4])

    def singleselect(self, i):
        self.selectRow(i)

    def multiselect(self, selectlist):
        for i in selectlist:
            self.selectRow(i)

    def resetRow(self, row):
        self.setRowCount(row)
        for i in xrange(self.rowCount()):
            self.setRowHeight(i, 250 / self.rowCount())
        # self.multiselect([2, 3, 4])

    def wheelEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            if self.currentRow() > 0: 
                self.clearSelection()
                self.singleselect(self.currentRow() - 1)
        elif event.key() == QtCore.Qt.Key_Down:
            if self.currentRow() < self.rowCount() - 1:
                self.clearSelection()
                self.singleselect(self.currentRow() + 1)
        elif event.key() == QtCore.Qt.Key_F1:
            import random
            self.resetRow(random.randint(0, 20))


class MainWindow(QtGui.QWidget):
    style = '''
        QWidget{
            background-color: black;
        }
         QScrollBar:vertical {
          border: 2px solid white;
          background: transparent;
          width: 25px;
          margin: 0 0 20px 0;
        }
        QScrollBar::handle:vertical {
            border: 1px solid black;
            background: white;
            height: 10px;
            max-height: 10px;
        }
      QScrollBar::add-line:vertical {
          background: transparent;
          height: 20px;
          width: 30px;
          subcontrol-position: bottom;
          subcontrol-origin: margin;
      }

      QScrollBar::sub-line:vertical {
          background: transparent;
      }
      QScrollBar::down-arrow:vertical {
         border-image: url(View/skin/PNG/downarrow.png);
      }

      QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
          background: none;
      }
      '''

    style2 = '''
    QWidget{
            background-color: black;
        }
      QScrollBar#mfd4scrollbar:vertical {
    border:10px, transparent;
    background: rgb(63, 70, 87);
    width: 26px;
    margin: 20px 5px 20px 5px;
}
QScrollBar#mfd4scrollbar::handle:vertical {
    background: rgb(108, 113, 125);
}
QScrollBar#mfd4scrollbar::add-line:vertical {
    background: transparent;
    height: 20px;
    width: 26px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar#mfd4scrollbar::sub-line:vertical {
    background: transparent;
    height: 20px;
    width: 26px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar#mfd4scrollbar::down-arrow:vertical {
    border-image: url(View/skin/PNG/downarrow_dash.png);
}

QScrollBar#mfd4scrollbar::up-arrow:vertical {
    border-image: url(View/skin/PNG/uparrow_dash.png);
}

QScrollBar#mfd4scrollbar::add-page:vertical, QScrollBar#mfd4scrollbar::sub-page:vertical {
    background: none;
}

    '''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(400, 300)

        self.scrollbar = ScrollBarWidget(20, self)
        self.scrollbar.move(20, 20)

        self.scrollbar2 = QtGui.QScrollBar(self)
        self.scrollbar2.setObjectName("mfd4scrollbar")
        self.scrollbar2.setOrientation(QtCore.Qt.Vertical)
        self.setStyleSheet(self.style2)
        self.scrollbar2.setFixedHeight(200)
        self.scrollbar2.move(100, 20)

        self.scrollbar2.setMinimum(0)
        self.scrollbar2.setMaximum(40)

        self.scrollbar2.setPageStep(40)

        self.scrollbar2.valueChanged.connect(self.changestyle)

    def changestyle(self, value):
        print value

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            if self.scrollbar.count < self.scrollbar.rowCount - 1:
                self.scrollbar.count += 1
        elif event.key() == QtCore.Qt.Key_Up:
            if self.scrollbar.count > 0:
                self.scrollbar.count -= 1
        elif event.key() == QtCore.Qt.Key_F1:
            import random
            rowcounrt = random.randint(1, 40)
            self.scrollbar.resetRow(rowcounrt)
            self.scrollbar.count = 0
            self.scrollbar2.setValue(rowcounrt)
        self.scrollbar.select(self.scrollbar.count)



class ScrollBarWidget(QtGui.QLabel):

    def __init__(self, row, parent=None):
        super(ScrollBarWidget, self).__init__(parent)
        self.rowCount = row
        self.setFixedSize(30, 212)
        self.arrowuplabel = QtGui.QLabel(self)
        self.arrowdownlabel = QtGui.QLabel(self)
        self.arrowuplabel.setFixedSize(26, 20)
        self.arrowdownlabel.setFixedSize(26, 20)
        self.arrowuplabel.setStyleSheet("QLabel{border-image: url(View/skin/PNG/uparrow_dash.png)}")
        self.arrowdownlabel.setStyleSheet("QLabel{border-image: url(View/skin/PNG/downarrow.png)}")
        self.arrowuplabel.move(2, 0)
        self.arrowdownlabel.move(2, 192)

        self.setStyleSheet("QLabel{background-color: rgb(49, 57, 78);}")

        self.blanky = 0
        self.blankx = 7

        self.starty = self.arrowuplabel.y() + self.arrowuplabel.height() + self.blanky
        self.startx = self.blankx

        self.endy = self.arrowdownlabel.y() - self.blanky
        self.height = self.endy - self.starty

        self.rectheight = (self.height - self.rowCount + 1) / self.rowCount
        self.rectwidth = self.width() - 2 * self.blankx

        self.selectlist = [0]
        self.count = 0

        self.resetRow(self.rowCount)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        color = QtGui.QColor(49, 57, 78)
        qp.setPen(color)
        for i in xrange(self.rowCount):
            if i in self.selectlist:
                qp.setBrush(QtGui.QColor(108, 113, 125))
            else:
                qp.setBrush(QtGui.QColor(63, 70, 87))
            y = self.starty + self.rectheight * i + i
            qp.drawRect(self.startx, y, self.rectwidth, self.rectheight)

    def select(self, i):
        self.selectlist = [i]
        self.update()

    def multiselect(self, selectlist):
        self.selectlist = selectlist
        self.update()

    def resetRow(self, row):
        self.rowCount = row
        self.rectheight = (self.height - self.rowCount) / self.rowCount
        self.update()

    def wheelEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass


class TreeWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.choices = [ str(i) for i in xrange(100)]
        self.radiobuttons = []
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setRowCount(len(self.choices))
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        self.table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        for index in range(len(self.choices)):
            radiobutton = QtGui.QRadioButton(self.choices[index])
            self.table.setCellWidget(index, 0, radiobutton)
            self.radiobuttons.append(radiobutton)
        self.radiobuttons[0].setChecked(True)

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.table)
        self.setLayout(mainlayout)


class TestWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)
        self.resize(400, 300)
        self.frame = QtGui.QFrame(self)
        self.frame.move(10, 10)
        self.frame.resize(200, 200)
        self.frame.setStyleSheet("QFrame{background-color:rgb(36, 43, 61); border-radius: 10px;}")

        for i in range(1, 4):
            setattr(self, 'text%d' % i, QtGui.QLabel(self.frame))
            label = getattr(self, 'text%d' % i)
            label.setText("%d" % i)
            label.setObjectName("AlertScreenText")
            # label.setFont(self.font)
            label.setAlignment(QtCore.Qt.AlignCenter)

        for i in range(1, 5):
            setattr(self, 'button%d' % i, QtGui.QPushButton('-', self.frame))
            button = getattr(self, 'button%d' % i)
            button.setObjectName("SoftButton")
            # button.setFont(self.font)

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.text1)
        mainlayout.addWidget(self.text2)
        mainlayout.addWidget(self.text3)
        softbuttonLayout = QtGui.QHBoxLayout()
        for i in range(1, 5):
            # getattr(self, "button%d" % i).setFixedSize(114, 40)
            softbuttonLayout.addWidget(getattr(self, "button%d" % i))

        mainlayout.addLayout(softbuttonLayout)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(mainlayout)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = TestWidget()
    main.show()
    sys.exit(app.exec_())
