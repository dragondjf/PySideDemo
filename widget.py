#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PySide.QtGui import *
from PySide.QtCore import *


def set_skin(QApplication, qssfile, style=''):
    qss = None
    with open(qssfile) as f:
        qss = ''.join(f.readlines()) + style
    QApplication.setStyleSheet(qss)


def setbg(widget, filename):
    '''
        设置背景颜色或者图片,平铺
    '''
    widget.setAutoFillBackground(True)
    palette = QPalette()
    pixmap = QPixmap(filename)
    pixmap = pixmap.scaled(widget.size())
    palette.setBrush(QPalette.Background, QBrush(pixmap))
    widget.setPalette(palette)


# def movecenter(w):
#     qr = w.frameGeometry()
#     cp = QtGui.QDesktopWidget().availableGeometry().center()
#     qr.moveCenter(cp)
#     w.move(qr.topLeft())


class CenterWindow(QWidget):

    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))  # 设置程序图标
        self.resize(800, 500)
        setbg(self, os.sep.join([os.getcwd(), "skin", "images", "bg.png"]))
        self.initUI()

    def createTitleBar(self):
        self.title_label = QLabel('dddd', self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet("color:white")

        self.title_icon_label = QLabel(self)
        self.title_icon_label.setPixmap(QPixmap(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))
        self.title_icon_label.setFixedSize(25, 25)
        self.title_icon_label.setScaledContents(True)

        self.close_button = QPushButton()
        self.close_button.setFixedHeight(30)
        self.close_button.setStyleSheet("border-image: url(skin/images/close.png)")

        #布局标题
        self.titlewidget = QWidget(self)
        self.title_layout = QHBoxLayout()
        self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label, 0, Qt.AlignLeft)
        self.title_layout.addStretch()   # 平均
        self.title_layout.addWidget(self.close_button, 0,  Qt.AlignTop)
        self.title_layout.setContentsMargins(5, 0, 0, 0)
        self.titlewidget.setLayout(self.title_layout)
        self.close_button.clicked.connect(self.close)

        setbg(self.titlewidget, os.sep.join([os.getcwd(), "skin", "images", "bg_dock.png"]))

    def initUI(self):
        self.createTitleBar()

        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(self.titlewidget)
        mainlayout.addStretch()
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        pass

    # def paintEvent(self, event):
    #     self.painter = QPainter()
    #     self.painter1 = QPainter()
    #     self.painter.begin(self)
    #     self.painter.drawPixmap(self.rect(), QPixmap("skin/images/bg.png"))
    #     self.painter.end()
    #     self.painter1.begin(self)
    #     self.painter1.drawPixmap(self.titlewidget.rect(), QPixmap("skin/images/bg_dock.png"))
    #     self.painter1.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = CenterWindow()
    main.show()
    sys.exit(app.exec_())
