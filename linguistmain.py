#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
module: main
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def tr(msg):
    return QCoreApplication.translate("@default", msg)

def main():
    app = QApplication([])

    trans = QTranslator()
    trans.load('plabel_zh_CN')
    app.installTranslator(trans)

    hello = QPushButton(tr("hello world!"))
    hello.show()

    app.exec_()
    
if __name__=="__main__":
    main()
