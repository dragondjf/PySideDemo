import os
from PySide import QtGui
from PySide import QtCore
from IconButton import IconButton
import socket


def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False


def valid_port(port):
    try:
        port = int(port)
        if port < 0 or port > 65535:
            return False
        else:
            return True
    except:
        return False


class TitleWidget(QtGui.QDialog):
    style = ""
    iconPath = os.sep.join([os.getcwd(), "View", "skin", "PNG", "icon.ico"])
    title = "title"

    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(self.iconPath))
        self.initUI()
        self.setStyleSheet(self.style)

    def initUI(self):
        self.createTitleBar()
        self.createCenterWidget()
        mainlayout = QtGui.QVBoxLayout(self)
        mainlayout.addWidget(self.titlewidget)
        mainlayout.addStretch()
        mainlayout.addWidget(self.centerwidget)
        mainlayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def createTitleBar(self):
        self.title_label = QtGui.QLabel(self.title, self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet("color:white")

        self.title_icon_label = QtGui.QLabel(self)
        self.title_icon_label.setPixmap(QtGui.QPixmap(os.sep.join([os.getcwd(), "skin", "PNG", "icon.ico"])))
        self.title_icon_label.setFixedSize(25, 25)
        self.title_icon_label.setScaledContents(True)

        self.close_button = QtGui.QPushButton()
        self.close_button.setFixedHeight(30)
        self.close_button.setStyleSheet("border-image: url(skin/PNG/close.png)")

        self.titlewidget = QtGui.QWidget(self)
        self.title_layout = QtGui.QHBoxLayout()
        self.title_layout.addWidget(self.title_icon_label, 0, QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.title_label, 0, QtCore.Qt.AlignLeft)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button, 0,  QtCore.Qt.AlignTop)
        self.title_layout.setContentsMargins(5, 0, 0, 0)

        self.titlewidget.setLayout(self.title_layout)
        self.close_button.clicked.connect(self.close)
        self.setbg(self.titlewidget, os.sep.join([os.getcwd(), "skin", "PNG", "bg_dock.png"]))

    def createCenterWidget(self):
        self.centerwidget = QtGui.QWidget()
        self.centerwidget.setObjectName("centerwidget")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()

    @staticmethod
    def setbg(widget, filename):
        widget.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        pixmap = QtGui.QPixmap(filename)
        pixmap = pixmap.scaled(widget.size())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        widget.setPalette(palette)


class FeedbackusDidalog(TitleWidget):
    title = "Feedback to US"
    style = '''
        QDialog{
            background-color: rgb(59,67,81);
        }

        QLabel{
            font:15px;
            color:white;
        }

        QLabel#tip{
            color: red;
            font-size:14px;
        }

        QLineEdit{
            height: 40px;
            width: 150px;
            border-image:url(skin/PNG/input.png);
            color:rgb(255,255,255);
            border:none;
            background-color:transparent;
            font-size:14px;
        }

        QTextEdit{
            border-image:url(skin/PNG/feedbackinput.png);
            color:rgb(255,255,255);
            border:none;
            background-color:transparent;
            font-size:14px;
        }

        QScrollBar:vertical
        {
            width:5px;
            background-color:hsva(255,255,255,0%);
        }
        QScrollBar::handle:vertical
        {
            /*background-color:hsva(200,200,200,20%);*/
            background-color:#252a31;
        }
        QScrollBar::add-line:vertical
        {
            background-color:hsva(255,255,255,0%);
            subcontrol-position:bottom;
        }
        QScrollBar::sub-line:vertical
        {
            background-color:hsva(255,255,255,0%);
            subcontrol-position:top;
        }
        QScrollBar::add-page:vertical
        {
            background:transparent;
        }
        QScrollBar::sub-page:vertical
        {
            background:transparent;
        }

        QScrollBar:horizontal
        {
        height:10px;
        background-color:hsva(255,255,255,0%);
        }
        QScrollBar::handle:horizontal
        {
            /*background-color:hsva(200,200,200,20%);*/
            background-color:#252a31;
        }
        QScrollBar::add-line:horizontal
        {
            background-color:hsva(255,255,255,0%);
            subcontrol-position:bottom;
        }
        QScrollBar::sub-line:horizontal
        {
            background-color:hsva(255,255,255,0%);
            subcontrol-position:top;
        }
        QScrollBar::add-page:horizontal
        {
            background:transparent;
        }
        QScrollBar::sub-page:horizontal
        {
            background:transparent;
        }
    '''

    def __init__(self, parent=None):
        super(FeedbackusDidalog, self).__init__(parent)
        # self.resize(500, 350)

    def createCenterWidget(self):
        self.centerwidget = QtGui.QWidget()
        self.centerwidget.setObjectName("centerwidget")

        self.name = QtGui.QLabel(self)
        self.name.setText("Name:")
        self.nameLineEdit = QtGui.QLineEdit(self)

        self.email = QtGui.QLabel(self)
        self.email.setText("Email:")

        self.emailLineEdit = QtGui.QLineEdit(self)

        self.telephone = QtGui.QLabel(self)
        self.telephone.setText("Telephone:")
        self.telephoneLineEdit = QtGui.QLineEdit(self)

        self.im = QtGui.QLabel(self)
        self.im.setText("IM:")

        self.imLineEdit = QtGui.QLineEdit(self)

        self.feedback = QtGui.QLabel(self)
        self.feedback.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.feedback.setText("FeedBack:")
        self.feedbackTextEdit = QtGui.QTextEdit(self)
        self.feedbackTextEdit.setMaximumHeight(128)

        self.errorTipLable = QtGui.QLabel()
        self.errorTipLable.setObjectName("tip")
        self.errorTipLable.hide()


        ok_up = os.sep.join([os.getcwd(), "skin", "PNG", "ok_up.png"])
        ok_down = os.sep.join([os.getcwd(), "skin", "PNG", "ok_down.png"])
        cancel_up = os.sep.join([os.getcwd(), "skin", "PNG", "cancel_up.png"])
        cancel_down = os.sep.join([os.getcwd(), "skin", "PNG", "cancel_down.png"])
        self.okButton = IconButton(ok_up, ok_down, "ok", self)
        self.cancelButton = IconButton(cancel_up, cancel_down, "cancel", self)

        mainlayout = QtGui.QGridLayout()
        mainlayout.addWidget(self.name, 0, 0)
        mainlayout.addWidget(self.nameLineEdit, 0, 1)
        mainlayout.addWidget(self.email, 0, 2)
        mainlayout.addWidget(self.emailLineEdit, 0, 3)

        mainlayout.addWidget(self.telephone, 1, 0)
        mainlayout.addWidget(self.telephoneLineEdit, 1, 1)
        mainlayout.addWidget(self.im, 1, 2)
        mainlayout.addWidget(self.imLineEdit, 1, 3)

        mainlayout.addWidget(self.feedback, 2, 0)
        mainlayout.addWidget(self.feedbackTextEdit, 2, 1, 1, 3)

        mainlayout.addWidget(self.errorTipLable, 3, 1, 1, 3)

        mainlayout.addWidget(self.okButton, 4, 1, 1, 2)
        mainlayout.addWidget(self.cancelButton, 4, 3, 1, 2)

        self.centerwidget.setLayout(mainlayout)

        self.okButton.clicked.connect(self.getFormData)
        self.cancelButton.clicked.connect(self.close)

    def getFormData(self):
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()
        telephone = self.telephoneLineEdit.text()
        im = self.imLineEdit.text()
        feedback = self.feedbackTextEdit.toPlainText()

        if feedback == "":
            self.errorTipLable.setText("Feedback is empty!")
            self.errorTipLable.show()
            return
        else:
            self.feedbackinfo = {
                "name": name,
                "email": email,
                "telephone": telephone,
                "im": im,
                "feedback": feedback
            }
            self.handleFormData(self.feedbackinfo)
            self.close()

    def handleFormData(self, data):
        print data


class AboutDialog(TitleWidget):

    style = '''
        QDialog{
            background-color: rgb(59,67,81);
        }
    '''
    title = "ALE"
    fulltitle = '''
    AppLink Emulator(ALE) 2.0.1'''

    copyright = '''
    (c) Copyright 2013, Ford Motor Company'''

    contentText = '''
    ALE is a non-hardware based solution to emulate 
    the in-vehicle interface between an AppLink 
    application and an equipped vehicle.This 
    software is provided AS IS, and is not intended 
    to replace proper testing with a SYNC Technology 
    Development Kit.
    '''

    extensionText = '''
    Software created using Python and pyside
    For more information visit the following links:\n 
        Python 2.7.5
            www.python.org\n
        Pyside 1.1.0 (LGPL License)
            www.pyside.org\n
        QT 4.8.5 (LGPL License)
             www.qt-project.org\n
    '''

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
    
    def createCenterWidget(self):
        self.centerwidget = QtGui.QWidget(self)

        titleLabel = QtGui.QLabel(self.fulltitle)
        copyrightLabel = QtGui.QLabel(self.copyright)
        contentTextLabel = QtGui.QLabel(self.contentText)
        self.extensionTextLabel = QtGui.QLabel(self.extensionText)
        self.licenseButton = IconButton(os.sep.join([os.getcwd(), \
            'skin', "PNG", "license_up.png"]), \
            os.sep.join([os.getcwd(), 'skin', "PNG", "license_down.png"]),\
             "License", self)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(copyrightLabel)
        mainLayout.addWidget(contentTextLabel)
        mainLayout.addWidget(self.licenseButton)
        mainLayout.addWidget(self.extensionTextLabel)
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.extensionTextLabel.hide()
        self.licenseButton.clicked.connect(self.showlicence)

        self.okButton = IconButton(os.sep.join([os.getcwd(), 'skin', "PNG", "ok_up.png"]), \
            os.sep.join([os.getcwd(), 'skin', "PNG", "ok_down.png"]), "Close", self)

        okButtonLayout = QtGui.QHBoxLayout() 
        okButtonLayout.addWidget(QtGui.QLabel())       
        okButtonLayout.addWidget(self.okButton)

        mainLayout.addLayout(okButtonLayout)
        self.centerwidget.setLayout(mainLayout)

        self.okButton.clicked.connect(self.close)

    def showlicence(self):
        if self.extensionTextLabel.isVisible():
            self.extensionTextLabel.hide()
        else:
            self.extensionTextLabel.show()


class FirstSettingDialog(TitleWidget):

    title = "FirstSetting"

    style = '''
        QDialog{
            background-color: rgb(59,67,81);
        }

        QLineEdit{
            height: 40px;
            width: 200px;
            border-image:url(skin/PNG/input.png);
            color:rgb(255,255,255); 
            border:none;
            background-color:transparent;
        }

        QLabel{
            color: white;
            font-size:14px;
        }

        QLabel#tip{
            color: red;
            font-size:14px;
        }
    '''

    def __init__(self, parent=None):
        super(FirstSettingDialog, self).__init__(parent)

    def createCenterWidget(self):
        self.centerwidget = QtGui.QWidget(self)
        self.ipLabel = QtGui.QLabel("Server IP: ")
        self.ipLineEdit = QtGui.QLineEdit()
        # self.ipLineEdit.setInputMask("000.000.000.000")

        self.portLabel = QtGui.QLabel("Server Port: ")
        self.portLineEdit = QtGui.QLineEdit()
        self.portLineEdit.setValidator(QtGui.QIntValidator(0, 65535))

        self.tipLabel = QtGui.QLabel("")
        self.tipLabel.setObjectName("tip")

        self.okButton = IconButton(os.sep.join([os.getcwd(), 'skin', "PNG", "ok_up.png"]), \
            os.sep.join([os.getcwd(), 'skin', "PNG", "ok_down.png"]), "ok", self)
        self.cancelButton = IconButton(os.sep.join([os.getcwd(), 'skin', "PNG", "cancel_up.png"]), \
            os.sep.join([os.getcwd(), 'skin', "PNG", "cancel_down.png"]), "cancel", self)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.ipLabel, 0, 0)
        mainLayout.addWidget(self.ipLineEdit, 0, 1, 1, 2)
        mainLayout.addWidget(self.portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1, 1, 2)
        mainLayout.addWidget(self.tipLabel, 2, 1, 1, 2)
        self.tipLabel.hide()

        okLayout = QtGui.QHBoxLayout()
        okLayout.addWidget(self.okButton)
        okLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(okLayout, 3, 0, 1, 3)
        self.centerwidget.setLayout(mainLayout)

        self.okButton.clicked.connect(self.getFormData)
        self.cancelButton.clicked.connect(self.close)

    def getFormData(self):
        ip = self.ipLineEdit.text()
        port = self.portLineEdit.text()
        ipvalid_flag = valid_ip(ip)
        portvalid_flag = valid_port(port)

        if ip == str(""):
            self.tipLabel.setText("Please input ip")
            self.tipLabel.show()
        elif not ipvalid_flag:
            self.tipLabel.setText("ip is not valid")
            self.tipLabel.show()
        elif port == str(""):
            self.tipLabel.setText("Please input port")
            self.tipLabel.show()
        elif not portvalid_flag:
                self.tipLabel.setText("port is not valid")
                self.tipLabel.show()
        else:
            self.address = (ip, port)
            self.handleFormData(self.address)
            self.close()

    def handleFormData(self, data):
        print data



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    feedback = FeedbackusDidalog()
    feedback.show()
    about = AboutDialog()
    about.show()
    firstsetting = FirstSettingDialog()
    firstsetting.show()
    sys.exit(app.exec_())
