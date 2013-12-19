import os
from PySide import QtGui
from PySide import QtCore
from IconButton import IconButton

class DIDDialog(QtGui.QDialog):

    style ='''
        QDialog{
                background-color: rgb(59,67,81);
        }
        QLabel{
            font:15px;
            color:white;
            text-align: center;
        }
        QLineEdit{
            height: 40px;
            width: 150px;
            border-image:url(View/skin/PNG/input.png);
            color:rgb(255,255,255);
            border:none;
            background-color:transparent;
            font-size:14px;
        }

    '''

    def __init__(self, parent=None):
        super(DIDDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        self.setWindowIcon(QtGui.QIcon(os.sep.join([os.getcwd(), "View", "skin", "PNG", "icon.ico"])))
        self.setWindowTitle("DID Data")
        self.setStyleSheet(self.style)
        self.resize(300, 150)
        self.initUI()

    def initUI(self):
        self.okButton = IconButton(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "ok_up.png"]), \
            os.sep.join([os.getcwd(), "View", 'skin', "PNG", "ok_down.png"]), "ok", self)
        self.cancelButton = IconButton(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cancel_up.png"]), \
            os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cancel_down.png"]), "cancel", self)

        okLayout = QtGui.QHBoxLayout()
        okLayout.addStretch()
        okLayout.addWidget(self.okButton)
        okLayout.addStretch()
        okLayout.addWidget(self.cancelButton)
        okLayout.addStretch()
        self.okButton.clicked.connect(self.savedata)
        self.cancelButton.clicked.connect(self.close)

        inputLayout = QtGui.QHBoxLayout()
        didLabel = QtGui.QLabel("DID Data")
        self.didLineEdit = QtGui.QLineEdit("")
        self.didLineEdit.setValidator(QtGui.QIntValidator(0, 100000000))
        inputLayout.addStretch()
        inputLayout.addWidget(didLabel)
        inputLayout.addStretch()
        inputLayout.addWidget(self.didLineEdit)
        inputLayout.addStretch()

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addLayout(inputLayout)
        mainlayout.addLayout(okLayout)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)

    def savedata(self):
        # self.model.saveModelData()
        # with open(self.jsonfilename, 'w') as f:
        #     json.dump(self.model.currentdata, f, indent=4)
        self.close()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = DIDDialog()
    main.show()
    sys.exit(app.exec_())
