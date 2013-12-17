from PySide import QtMultimedia
from PySide import QtCore
from PySide import QtGui


class ALESingle(QtCore.QObject):

    notification = QtCore.Signal(list)

    def __init__(self):
        super(ALESingle, self).__init__()


alesingle = ALESingle()


class AudioRecordThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(AudioRecordThread, self).__init__(parent)
        self.initAudio()
        self.databuffer = []

        self.terminated.connect(self.senddata)

    def initAudio(self):
        format = QtMultimedia.QAudioFormat()
        format.setChannelCount(1)
        format.setSampleRate(96000)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setSampleType(QtMultimedia.QAudioFormat.UnSignedInt)

        self.audiodevice = QtMultimedia.QAudioDeviceInfo.defaultInputDevice()
        if not self.audiodevice.isFormatSupported(format):
            format = self.audiodevice.nearestFormat(format)

        self.audio = QtMultimedia.QAudioInput(self.audiodevice, format, self)
        self.audio.setNotifyInterval(1000)
        self.audio.notify.connect(self.senddata)

    def run(self):
        self.iodevice = self.audio.start()
        self.iodevice.readyRead.connect(self.handleReadyRead)
        self.exec_()

    def handleReadyRead(self):
        self.databuffer.append(self.iodevice.readAll().data())

    def senddata(self):
        # print len(self.databuffer)
        # data = ''.join(self.databuffer)
        alesingle.notification.emit(self.databuffer)
        self.databuffer = []


class AudioRecord(QtGui.QWidget):

    def __init__(self, parent=None):
        super(AudioRecord, self).__init__(parent)
        self.audiorecordthread = AudioRecordThread()
        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.stopRecording)
        self.timer.start()

    def initUI(self):
        pass

    def startRecording(self):
        self.audiorecordthread.start()

    def stopRecording(self):
        self.close()

    def closeEvent(self, event):
        self.audiorecordthread.audio.stop()
        # self.audiorecordthread.exit(0)
        self.audiorecordthread.terminate()
        self.timer.stop()
        print self.audiorecordthread.isFinished()


class Mainwindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.startButton = QtGui.QPushButton("start")
        self.stopButton = QtGui.QPushButton("stop")
        mainlayout = QtGui.QHBoxLayout()
        mainlayout.addWidget(self.startButton)
        # mainlayout.addWidget(self.pauseButton)
        mainlayout.addWidget(self.stopButton)
        self.setLayout(mainlayout)

        self.startButton.clicked.connect(self.startRecording)
        self.stopButton.clicked.connect(self.stopRecording)

        alesingle.notification.connect(self.handledata)

    def startRecording(self):
        self.audiodialog = AudioRecord()
        self.audiodialog.startRecording()
        self.audiodialog.show()

    def stopRecording(self):
        if hasattr(self, 'audiodialog'):
            self.audiodialog.close()
            del self.audiodialog

    @QtCore.Slot(list)
    def handledata(self, data):
        print len(data), len(''.join(data))



def getAvailableDevices():
    devices = QtMultimedia.QAudioDeviceInfo.availableDevices(QtMultimedia.QAudio.AudioInput)
    for dev in devices:
        print dev.supportedCodecs()
        print dev.supportedSampleRates()
        print dev.supportedSampleSizes()
        print dev.supportedSampleTypes()
        a = dev.deviceName()
        print a
    return devices

if __name__ == '__main__':
    import sys
    # print getAvailableDevices()
    app = QtGui.QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec_())
