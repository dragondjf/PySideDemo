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

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(400, 300)

        self.scrollbar = ScrollBarWidget(20, self)
        self.scrollbar.move(20, 20)

        self.scrollbar2 = QtGui.QScrollBar(self)
        self.scrollbar2.setOrientation(QtCore.Qt.Vertical)
        self.setStyleSheet(self.style)
        self.scrollbar2.setFixedHeight(200)
        self.scrollbar2.move(100, 20)

        self.scrollbar2.setMinimum(0)
        self.scrollbar2.setMaximum(40)

        self.scrollbar2.setPageStep(40)

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

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
