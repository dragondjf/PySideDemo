#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide import QtCore
import os
import copy
import time


class ScrollBar(QtGui.QTableWidget):

    style = '''
        /*border: 2px solid #485260;*/
        /*border: none;*/
        /*color: white;*/
        background-color: rgb(48, 55, 72);
        /*selection-color: #252a31;*/
        selection-background-color:rgb(108,113,125);
    '''

    def __init__(self, row, height=200, parent=None):
        super(ScrollBar, self).__init__(row, 1, parent)
        self.setFixedSize(15, height)
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
            self.setRowHeight(i, self.height() / self.rowCount())
        self.selectRow(self.currentRow())
    def singleselect(self, i):
        self.selectRow(i)

    def multiselect(self, selectlist):
        for i in selectlist:
            self.selectRow(i)

    def resetRow(self, row):
        self.setRowCount(row)
        for i in xrange(self.rowCount()):
            self.setRowHeight(i, self.height() / self.rowCount())
        self.selectRow(self.currentRow())

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

    def upline(self):
        if self.currentRow() > 0: 
            self.clearSelection()
            self.singleselect(self.currentRow() - 1)

    def downline(self):
        if self.currentRow() < self.rowCount() - 1:
            self.clearSelection()
            self.singleselect(self.currentRow() + 1)

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


def setbg(widget, filename):
    '''
        设置背景颜色或者图片,平铺
    '''
    widget.setAutoFillBackground(True)
    palette = QtGui.QPalette()
    pixmap = QtGui.QPixmap(filename)
    pixmap = pixmap.scaled(widget.size())
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
    widget.setPalette(palette)


class IconButton(QtGui.QPushButton):

    style = '''
        QPushButton{
            border: None;
        }
    '''
    buttonEventName = {
        "0": "PRESET_0",
        "1": "PRESET_1",
        "2": "PRESET_2",
        "3": "PRESET_3",
        "4": "PRESET_4",
        "5": "PRESET_5",
        "6": "PRESET_6",
        "7": "PRESET_7",
        "8": "PRESET_8",
        "9": "PRESET_9",
        "ok": "OK"
    }

    def __init__(self, button_id, postion, parent=None):
        super(IconButton, self).__init__(parent)
        self.parent = parent
        images_path = os.sep.join([os.getcwd(), "View", 'skin', 'PNG'])
        button_id_up = "button_%s_up" % button_id
        button_id_down = "button_%s_down" % button_id
        up = os.sep.join([images_path, "%s.png" % button_id_up])
        down = os.sep.join([images_path, "%s.png" % button_id_down])
        self.name = button_id
        self.postion = postion
        self.timePress = 0
        self.timeRelease = 0

        self.pixmap_up = QtGui.QPixmap(up)
        self.pixmap_down = QtGui.QPixmap(down)
        self.icon_up = QtGui.QIcon(self.pixmap_up)
        self.icon_down = QtGui.QIcon(self.pixmap_down)
        self.setObjectName(button_id)
        self.setIcon(self.icon_up)

        self.setIconSize(self.pixmap_up.size())
        self.setFixedSize(self.pixmap_up.size())
        self.resize(self.pixmap_up.size())
        self.setStyleSheet(self.style)

        self.move(self.postion)

        self.pressed.connect(self.actionPress)
        self.released.connect(self.actionRelease)

    def mouseDoubleClickEvent(self, event):
        print "mouseDoubleClickEvent"

    def actionPress(self):
        self.timePress = time.time()
        self.setIcon(self.icon_down)

    def actionRelease(self):
        self.timeRelease = time.time()
        self.setIcon(self.icon_up)

    def action(self):
        if self.name in self.buttonEventName:
            name = self.buttonEventName[self.name]
            sptime = self.timeRelease - self.timePress
            mode = "SHORT"
            if sptime > 2:
                mode = "LONG"
            data = {"mode": mode, "name": name}


class ControlPanel(QtGui.QGraphicsView):

    leftbuttons = ["cd", "radio", "aux", "phone", "menu", "left_down_1", "left_down_2"]
    middleButtons = ["left", "right", "up", "down", "ok", "pre", "next"]
    rightbuttons = [["ta", "music"], ["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["X", "0", "H"], ["right_down_1", "right_down_2"]]

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self.parent = parent
        self.bg = QtGui.QPixmap(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "01.png"]))
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setMinimumHeight(288)
        self.setMaximumHeight(288)
        self.setMaximumWidth(530)
        self.setMinimumWidth(530)
        # self.move(3, 300)
        self.initUI()

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(os.sep.join([os.getcwd(), "View", 'skin', "PNG", "01.png"]))))

    def initUI(self):
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene.setSceneRect(0, 0, self.bg.width(), self.bg.height())
        self.setScene(self.scene)

        self.createButtons()
        # self.createButtonSlots()

    def createButtons(self):
        for button_id in self.leftbuttons:
            i = self.leftbuttons.index(button_id)
            if i < 5:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(10, 14 + i * 45), self))
            elif i == 5:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(12, 14 + 5 * 45), self))
            elif i == 6:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(92, 14 + 5 * 45), self))

        for button_id in self.middleButtons:
            i = self.middleButtons.index(button_id)
            if i == 0:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(191, 40), self))
            if i == 1:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(260, 39), self))
            if i == 2:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(209, 21), self))
            if i == 3:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(209, 88), self))
            if i == 4:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(213, 46), self))
            if i == 5:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(212, 161), self))
            if i == 6:
                setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(273, 161), self))

        for buttons in self.rightbuttons:
            i = self.rightbuttons.index(buttons)
            for button_id in buttons:
                j = buttons.index(button_id)
                if i == 0:
                    setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(360 + 80 * j, 14), self))
                if i > 0 and i < 5:
                    setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(360 + 55 * j, 14 + i * 45), self))
                elif i == 5:
                    setattr(self, "button_%s" % button_id, IconButton(button_id, QtCore.QPoint(360 + 80 * j, 14 + i * 45), self))

    def createButtonSlots(self):
        for button_id in self.leftbuttons:
            self.slotByButtonId(button_id)

        for button_id in self.middleButtons:
            self.slotByButtonId(button_id)

        for buttons in self.rightbuttons:
            for button_id in buttons:
                self.slotByButtonId(button_id)

    def slotByButtonId(self, button_id):
        buttonObj = getattr(self, "button_%s" % button_id)
        action = getattr(buttonObj, "action")
        getattr(self, "button_%s" % button_id).clicked.connect(action)

    def action_NotImplement(self):
        print "action_NotImplement"




class TextScreen(QtGui.QTextEdit):

    style = '''
    QTextEdit{
        color: white;
        border: 5px;
        selection-color: green;
        selection-background-color: #252a31;
        background-attachment: fixed;
    }
    '''
    fontFilePath = os.sep.join([os.getcwd(), 'View', 'skin', "font", "HelveticaNeueLTCom-LtCn.ttf"])
    limit_linecharnum = 15


    def __init__(self, parent=None):
        super(TextScreen, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        # self.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.setMouseTracking(False)
        self.parent = parent
        pl = QtGui.QPalette(self.palette())
        pl.setBrush(QtGui.QPalette.Base, QtGui.QBrush(QtGui.QColor(255, 0, 0, 0)))
        self.setPalette(pl)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)
        self.setStyleSheet(self.style)
        self.setfont()
        self.resize(490, 200)

        self.currentLineNumber = 0
        self.currentLineText = ""

        self.cursorPositionChanged.connect(self.high_light_current_line)
        self.textcursor = self.textCursor()
        self.textcursor.movePosition(QtGui.QTextCursor.Start)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)
        self.setObjectName("Screen")

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
        flag = False
        if self.currentLineNumber == len(self.text) - 1:
            flag = True
        if flag:
            self.textcursor.movePosition(QtGui.QTextCursor.Start)
        else:
            self.textcursor.movePosition(QtGui.QTextCursor.Down)
        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)
        self.currentLineNumber = self.textCursor().blockNumber()
        self.currentLineText = self.textcursor.selectedText()

    def initText(self, text):
        self.text = copy.deepcopy(text)
        oldtext = copy.deepcopy(text)
        for i in xrange(0, len(oldtext)):
            if len(oldtext[i]) > self.limit_linecharnum:
                limitcontent = oldtext[i][0:self.limit_linecharnum] + '...'
                oldtext[i] = limitcontent
        textstring = "\n".join(oldtext)
        self.setPlainText(textstring)
        self.textcursor.movePosition(QtGui.QTextCursor.Start)

        self.textcursor.select(QtGui.QTextCursor.LineUnderCursor)
        self.setTextCursor(self.textcursor)

        self.currentLineNumber = self.textCursor().blockNumber()
        self.currentLineText = self.textcursor.selectedText()

    def insertLine(self, row, content):
        self.text.insert(row, content)
        oldtext = copy.deepcopy(self.text)
        for i in xrange(0, len(oldtext)):
            if len(oldtext[i]) > self.limit_linecharnum:
                limitcontent = oldtext[i][0:self.limit_linecharnum] + '...'
                oldtext[i] = limitcontent
        self.initText(oldtext)

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


class BaseSceen(QtGui.QWidget):

    def __init__(self, parent=None):
        super(BaseSceen, self).__init__(parent)
        self.fixedsize()

    def fixedsize(self):
        self.setMinimumHeight(298)
        self.setMaximumHeight(298)
        self.setMaximumWidth(534)
        self.setMinimumWidth(534)


class AppScreen(BaseSceen):

    def __init__(self, parent=None):
        super(AppScreen, self).__init__(parent)
        self.parent = parent
        self.id = "appscreen"
        self.initUI()
        setbg(self, os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cleanscreen.png"]))

    def initUI(self):
        self.textsceen = TextScreen(self)
        self.textsceen.initText(['app1', 'app2', 'app1', 'app2'])
        self.textsceen.move(16, 62)
        self.textsceen.setMinimumHeight(220)
        self.textsceen.setMaximumHeight(220)
        self.textsceen.setMaximumWidth(502)
        self.textsceen.setMinimumWidth(502)

        self.scrollbar = ScrollBar(16, 200, self)
        self.scrollbar.move(490, 70)

    def action_leftclick(self):
        pass

    def action_rightclick(self):
        self.parent.swicthscreen("mfdscreen")

    def action_upclick(self):
        self.textsceen.upline()
        self.scrollbar.upline()
    def action_downclick(self):
        self.textsceen.downline()
        self.scrollbar.downline()

    def action_okclick(self):
        import random
        l = random.randint(0, 20)
        texts = []
        for i in xrange(l):
            texts.append('app%d' % i)
        self.textsceen.initText(texts)
        self.scrollbar.resetRow(l)


class MFDScreen(BaseSceen):

    def __init__(self, parent=None):
        super(MFDScreen, self).__init__(parent)
        self.parent = parent
        self.id = "mfdscreen"
        self.initUI()
        setbg(self, os.sep.join([os.getcwd(), "View", 'skin', 'PNG', 'appscreen.png']))

    def initUI(self):
        self.textsceen = TextScreen(self)
        self.textsceen.initText(['mfd1', 'mfd2'])
        self.textsceen.move(100, 70)
        self.textsceen.setMinimumHeight(113)
        self.textsceen.setMaximumHeight(113)
        self.textsceen.setMaximumWidth(410)
        self.textsceen.setMinimumWidth(410)

    def action_leftclick(self):
        self.parent.swicthscreen('appscreen')

    def action_rightclick(self):
        self.parent.swicthscreen("menuscreen")

    def action_upclick(self):
        self.textsceen.upline()

    def action_downclick(self):
        self.textsceen.downline()

    def action_okclick(self):
        pass


class MenuScreen(BaseSceen):

    def __init__(self, parent=None):
        super(MenuScreen, self).__init__(parent)
        self.parent = parent
        self.id = "menuscreen"
        self.initUI()
        setbg(self, os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cleanscreen.png"]))

    def initUI(self):
        self.textsceen = TextScreen(self)
        self.textsceen.initText(['menu1', 'menu2'])
        self.textsceen.move(16, 62)
        self.textsceen.setMinimumHeight(220)
        self.textsceen.setMaximumHeight(220)
        self.textsceen.setMaximumWidth(502)
        self.textsceen.setMinimumWidth(502)

        self.scrollbar = ScrollBar(4, 1, self)
        self.scrollbar.move(500, 50)

    def action_leftclick(self):
        self.parent.swicthscreen('mfdscreen')

    def action_rightclick(self):
        self.parent.swicthscreen('childmenuscreen')

    def action_upclick(self):
        self.textsceen.upline()

    def action_downclick(self):
        self.textsceen.downline()

    def action_okclick(self):
        pass



class ChildMenuScreen(BaseSceen):

    def __init__(self, parent=None):
        super(ChildMenuScreen, self).__init__(parent)
        self.parent = parent
        self.id = "childmenuscreen"
        self.initUI()
        setbg(self, os.sep.join([os.getcwd(), "View", 'skin', "PNG", "cleanscreen.png"]))

    def initUI(self):
        self.textsceen = TextScreen(self)
        self.textsceen.initText(['chiledmenu1', 'chiledmenu2'])
        self.textsceen.move(16, 62)
        self.textsceen.setMinimumHeight(220)
        self.textsceen.setMaximumHeight(220)
        self.textsceen.setMaximumWidth(502)
        self.textsceen.setMinimumWidth(502)

    def action_leftclick(self):
        self.parent.swicthscreen('menuscreen')

    def action_rightclick(self):
        self.parent.swicthscreen('menuscreen')

    def action_upclick(self):
        self.textsceen.upline()

    def action_downclick(self):
        self.textsceen.downline()

    def action_okclick(self):
        pass


class CenterWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.parent = parent
        self.initUI()
        self.fixedsize()
        setbg(self, os.sep.join([os.getcwd(), "View", 'skin', 'PNG', 'bg.png']))

    def initUI(self):
        self.screens = QtGui.QStackedWidget()  # 创建堆控件
        self.appscreen = AppScreen(self)
        self.mfdscreen = MFDScreen(self)
        self.menuscreen = MenuScreen(self)
        self.childmenuscreen = ChildMenuScreen(self)

        self.screenslist = [self.appscreen, self.mfdscreen, self.menuscreen, self.childmenuscreen]

        self.screens.addWidget(self.appscreen)
        self.screens.addWidget(self.mfdscreen)
        self.screens.addWidget(self.menuscreen)
        self.screens.addWidget(self.childmenuscreen)


        self.controlpannel = ControlPanel(self)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.screens)
        mainLayout.addWidget(self.controlpannel)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

        for item in ["left", "up", "right", "down", "ok"]:
            action = getattr(self.appscreen, "action_%sclick" % item)
            getattr(self.controlpannel, "button_%s" % item).clicked.connect(action)

    def swicthscreen(self, screen):
        n = getattr(self, screen)
        self.screens.setCurrentWidget(n)
        for item in ["left", "up", "right", "down", "ok"]:
            getattr(self.controlpannel, "button_%s" % item).clicked.disconnect()
            if hasattr(n , "action_%sclick" % item):
                action = getattr(n, "action_%sclick" % item)
                getattr(self.controlpannel, "button_%s" % item).clicked.connect(action)

    def fixedsize(self):
        self.setMinimumHeight(596)
        self.setMaximumHeight(596)
        self.setMaximumWidth(534)
        self.setMinimumWidth(534)



if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    screen = CenterWindow()
    screen.show()
    sys.exit(app.exec_())
