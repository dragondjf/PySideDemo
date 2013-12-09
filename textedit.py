from PySide import QtGui
from PySide import QtCore
import os
import copy
import random


class SingleSlotManager(QtCore.QObject):

    intdata = QtCore.Signal(int)
    listdata = QtCore.Signal(list)
    dictdata = QtCore.Signal(dict)
    int_str_data = QtCore.Signal(int, str)

    def __init__(self, mainwidget):
        super(SingleSlotManager, self).__init__()
        self.int_str_data.connect(mainwidget.insertLine)


class AppThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(AppThread, self).__init__(None)

    def run(self):
        self.exec_()


class TextScreen(QtGui.QTextEdit):

    style = '''
    QTextEdit{
        color: white;
        background-color: #3b4351;
        border: none;
        selection-color: green;
        selection-background-color: #252a31;
        background-image: url(skin/PNG/bg.png);
        background-attachment: fixed;
    }
    '''
    fontFilePath = os.sep.join([os.getcwd(), 'skin', "font", "HelveticaNeueLTCom-LtCn.ttf"])

    limit_linecharnum = 15

    def __init__(self, parent=None):
        super(TextScreen, self).__init__(parent)
        self.parent = parent
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setStyleSheet(self.style)
        self.setfont()
        self.resize(490, 200)

        self.text = ['1', '22', '333', '4444', '55555']
        self.currentLineNumber = 0
        self.currentLineText = ""

        self.updateText(self.text)
        self.cursorPositionChanged.connect(self.high_light_current_line)
        self.textcursor = self.textCursor()
        self.textcursor.movePosition(QtGui.QTextCursor.Start)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)

    def setfont(self):
        fontid = QtGui.QFontDatabase.addApplicationFont(self.fontFilePath)
        f = list(QtGui.QFontDatabase.applicationFontFamilies(fontid))[0]
        self.setFont(QtGui.QFont(f, 30))

    def high_light_current_line(self):
        extra_selections = []
        selection = QtGui.QTextEdit.ExtraSelection()
        line_color = QtGui.QColor("#252a31")
        selection.format.setBackground(line_color)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def upline(self):
        self.textcursor.movePosition(QtGui.QTextCursor.Up)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)
        self.currentLineNumber = self.textCursor().blockNumber()
        self.currentLineText = self.textcursor.selectedText()

    def downline(self):
        self.textcursor.movePosition(QtGui.QTextCursor.Down)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)
        self.currentLineNumber = self.textCursor().blockNumber()
        self.currentLineText = self.textcursor.selectedText()

    def updateText(self, text):
        textstring = "\n".join(text)
        self.setPlainText(textstring)

    @QtCore.Slot(int, str)
    def insertLine(self, row, content):
        self.text.insert(row, content)
        oldtext = copy.deepcopy(self.text)
        for i in xrange(0, len(oldtext)):
            if len(oldtext[i]) > self.limit_linecharnum:
                limitcontent = content[0:self.limit_linecharnum] + '...'
                oldtext[i] = limitcontent
        self.updateText(oldtext)

        self.textcursor.movePosition(QtGui.QTextCursor.Start)
        for i in xrange(row):
            self.textcursor.movePosition(QtGui.QTextCursor.Down)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)

        self.currentLineNumber = self.textCursor().blockNumber()
        self.currentLineText = self.textcursor.selectedText()

    def getCurrentLineNumber(self):
        return self.currentLineNumber

    def getCurrentLineText(self):
        return self.currentLineText

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.upline()
        if event.key() == QtCore.Qt.Key_Down:
            self.downline()
        if event.key() == QtCore.Qt.Key_I:
            self.insertLine(random.randint(0, 6), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print self.getCurrentLineNumber(), self.getCurrentLineText()
        print self.text


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = TextScreen()
    main.show()
    ssmanger = SingleSlotManager(main)
    ssmanger.int_str_data.emit(2, "ssssss")
    sys.exit(app.exec_())
