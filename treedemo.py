
import os
from PySide import QtCore
from PySide import QtGui
import json

vehicleData = {
    'speed': 80.0,
    'rpm': 5000,
    'fuelLevel': 0.2,
    'fuelLevel_State': "UNKNOWN",
    'instantFuelConsumption': 2.2,
    'tirePressure': "UNKNOWN",
    'beltStatus': {
        'driverBeltDeployed': "NOT_SUPPORTED",
        'passengerBeltDeployed': "NOT_SUPPORTED",
        'passengerBuckleBelted': "NOT_SUPPORTED",
        'driverBuckleBelted': "NOT_SUPPORTED",
        'leftRow2BuckleBelted': "NOT_SUPPORTED",
        'passengerChildDetected': "NOT_SUPPORTED",
        'rightRow2BuckleBelted': "NOT_SUPPORTED",
        'middleRow2BuckleBelted': "NOT_SUPPORTED",
        'middleRow3BuckleBelted': "NOT_SUPPORTED",
        'leftRow3BuckleBelted': "NOT_SUPPORTED",
        'rightRow3BuckleBelted': "NOT_SUPPORTED",
        'leftRearInflatableBelted': "NOT_SUPPORTED",
        'rightRearInflatableBelted': "NOT_SUPPORTED",
        'middleRow1BeltDeployed': "NOT_SUPPORTED",
        'middleRow1BuckleBelted': "NOT_SUPPORTED"
    },
    'bodyInformation': {
        'parkBrakeActive': False,
        'ignitionStableStatus': "MISSING_FROM_TRANSMITTER",
        'ignitionStatus': "UNKNOWN"
    },
    'deviceStatus': {
        'voiceRecOn': False,
        'btIconOn': False,
        'callActive': False,
        'phoneRoaming': False,
        'textMsgAvailable': False,
        'battLevelStatus': "NOT_PROVIDED",
        'stereoAudioOutputMuted': False,
        'monoAudioOutputMuted': False,
        'signalLevelStatus': "NOT_PROVIDED",
        'primaryAudioSource': "NO_SOURCE_SELECTED",
        'eCallEventActive': False
    },
    'driverBraking': "NOT_SUPPORTED",
    'wiperStatus': "NO_DATA_EXISTS",
    'headLampStatus': {
        "lowBeamsOn": False,
        "highBeamsOn": False
    },
    'engineTorque': 2.5,
    'accPedalPosition': 0.5,
    'steeringWheelAngle': 1.2,
    'myKey': {
        "e911Override": "NO_DATA_EXISTS"
    },
    'avgFuelEconomy': 0.1,
    'batteryVoltage': 12.5,
    'externalTemperature': 40.0,
    'vin': '52-452-52-752',
    'prndl': 'PARK',
    'batteryPackVoltage': 12.5,
    'batteryPackCurrent': 7.0,
    'batteryPackTemperature': 30,
    'engineTorque': 650,
    'tripOdometer': 0,
    'genericbinary': '165165650',
    'satRadioESN': "165165650",
    'rainSensor': 165165650,
    'gps': {
        'longitudeDegrees': 423293,
        'latitudeDegrees': -830464,
        'utcYear': 2013,
        'utcMonth': 2,
        'utcDay': 14,
        'utcHours': 13,
        'utcMinutes': 16,
        'utcSeconds': 54,
        'compassDirection': 'SOUTHWEST',
        'pdop': 15,
        'hdop': 5,
        'vdop': 30,
        'actual': False,
        'satellites': 8,
        'dimension': '2D',
        'altitude': 7,
        'heading': 173,
        'speed': 2
    },
    'a':{
        1: 1111,
        'b': {
            2: 22222,
            'c': 3333
        }
    }
}

with open('data.json', 'w') as f:
    json.dump(vehicleData, f, indent=4)

class TreeItem(object):
    
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def child(self, row):
        return self.childItems[row]
 
    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.insert(position, None)

        for child in self.childItems:
            child.insertColumns(position, columns)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.pop(position)

        for child in self.childItems:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, headers, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.primarydata = data
        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.rootItem.columnCount()

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0
        if index.column() == 0 or index.column() == 1:
            return 0
        elif index.isValid():
            item = index.internalPointer()
            if item.itemData[1] == "":
                return 0
            else:
                return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setupModelData(self, data, parent):
        createItem(data, parent)

    def saveModelData(self):
        self.currentdata = readfromItem(self.rootItem, {})


def readfromItem(parentItem, data={}):
    for item in parentItem.childItems:
        if len(item.childItems) > 0:
            key = item.itemData[0]
            data.update({key: {}})
            readfromItem(item, data[key])
        else:
            key = item.itemData[0]
            value = item.itemData[2]
            data.update({key: value})
    return data

def createItem(data, parentItem):
    if isinstance(data, dict):
        for key in data.keys():
            if isinstance(data[key], dict):
                itemdata = [key, '', '']
            else:
                itemdata = [key, str(type(data[key]))[7: -2], data[key]]
            item = TreeItem(itemdata, parentItem)
            parentItem.childItems.append(item)
            createItem(data[key], item)
    return parentItem


class TreeDemo(QtGui.QDialog):
    style = '''
    QDialog{
            background-color: rgb(59,67,81);
    }

    QHeaderView::section {
        background-color: #3b4351;
        color: white;
        padding-left: 4px;
        border: 1px solid #6c6c6c;
     }

    QHeaderView::section:checked {
        background-color: #112233;
     }

    QHeaderView::section:checked {
        background-color: white;
    }

    QHeaderView{
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #485260, stop: 0.5 #252a31,
                                           stop: 0.6 #252a31, stop:1 #485260);
    }

    QHeaderView::section {
        /*background-color: #252a31;*/
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #485260, stop: 0.5 #252a31,
                                           stop: 0.6 #252a31, stop:1 #485260);
        color: white;
        padding-left: 4px;
        border: 1px solid #252a31;
     }

    QTreeView {
        /*border: 1px solid #485260;*/
        /*border: none;*/
        color: white;
        background-color: #5B677A;
        alternate-background-color: yellow;
        /*selection-background-color:#485260;*/
    }

    QTreeView::item {
        border: none;
        border-top-color: transparent;
        border-bottom-color: transparent;
    }
    QTreeView::item:hover {
        border: 1px solid transparent;
        background-color: green;
    }

    QTreeView::item:selected {
        border: 1px solid transparent;
        background-color: green;
    }


    QScrollBar:vertical
    {
        width:10px;
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
    def __init__(self, jsonfilename=None,parent=None):
        super(TreeDemo, self).__init__(parent)
        self.setWindowTitle("Custom Data")
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        # self.setWindowIcon(QtGui.QIcon(os.sep.join([os.getcwd(), "View", "skin", "PNG", "icon.ico"])))
        self.resize(600, 400)
        self.setStyleSheet(self.style)

        self.jsonfilename = os.sep.join([os.getcwd(), "data.json"])
        self.initData()
        self.initUI()

    def initData(self):
        with open(self.jsonfilename, 'r') as f:
            self.data = json.load(f)
        headers = ['Key', 'Type', 'Value']
        self.model = TreeModel(headers, self.data)
        self.treeview = QtGui.QTreeView()
        self.treeview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.treeview.setFocusPolicy(QtCore.Qt.NoFocus)
        self.treeview.setModel(self.model)
        self.treeview.setColumnWidth(0, 250)
        self.treeview.setColumnWidth(1, 100)
        self.treeview.setColumnWidth(2, 200)

    def initUI(self):
        self.okButton = QtGui.QPushButton('Save')
        self.cancelButton = QtGui.QPushButton('Cancel')
        okLayout = QtGui.QHBoxLayout()
        okLayout.addStretch()
        okLayout.addWidget(self.okButton)
        okLayout.addStretch()
        okLayout.addWidget(self.cancelButton)
        okLayout.addStretch()
        self.okButton.clicked.connect(self.savedata)
        self.cancelButton.clicked.connect(self.close)

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.treeview)
        mainlayout.addLayout(okLayout)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)

    def savedata(self):
        self.model.saveModelData()
        with open(self.jsonfilename, 'w') as f:
            json.dump(self.model.currentdata, f, indent=4)
        self.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    treedemo = TreeDemo()
    treedemo.show()
    sys.exit(app.exec_())
