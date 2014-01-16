import os
import Log
from Log import logSignal 
import logging
from PySide import QtGui
from PySide import QtCore

logger = logging.getLogger(__file__)

class QLogBrowser(QtGui.QTextEdit):

    style = '''
    QTextEdit{
        border-image:url(View/skin/PNG/feedbackinput.png);
        color:rgb(255,255,255);
        border:none;
        background-color:transparent;
        font-size:14px;
    }
    '''

    def __init__(self, parent=None):
        self.parent = parent
        super(QLogBrowser, self).__init__(parent)
        self.resize(500, 500)
        # print self.style
        self.setStyleSheet(self.style)
        logSignal.onelogsin.connect(self.addOneLog)
        logger.info('1111111111111')

    def addOneLog(self, onemessage):
        self.append(onemessage)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 600)
        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.addlogbytimer)
        self.timer.start()

    def initUI(self):
        self.logbrowser = QLogBrowser()
        self.logbutton = QtGui.QPushButton("Log", self)
        self.logbutton.move(100, 100)
        self.logbutton.clicked.connect(self.logshow)

    def logshow(self):
        self.logbrowser.show()

    def addlogbytimer(self):
        # logger.debug('*' * 50)
        logger.info('*' * 50)
        logger.warning('*' * 50)
        logger.error('*' * 50)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
