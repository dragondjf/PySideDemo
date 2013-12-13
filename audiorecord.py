from PySide import QtMultimedia
from PySide import QtCore
from PySide import QtGui


class AudioIODevice(QtCore.QIODevice):

    def __init__(self, parent=None):
        super(AudioIODevice, self).__init__(parent)
        print self.open(QtCore.QIODevice.ReadWrite)
        self.readyRead.connect(self.handledata)
    # def writeData(self, data, s):
    #     a = self.write(data)
    #     # print type(data), s
    #     return a

    def handledata(self):
        print '------------'


class AudioRecord(QtGui.QDialog):

    def __init__(self, parent=None):
        super(AudioRecord, self).__init__(parent)
        self.initAudio()
        self.initUI()

    def initAudio(self):
        self.audiofile = QtCore.QFile()
        self.audiofile.setFileName("testMicIn.wav")
        self.audiofile.open(QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Truncate)
        self.audiofile.readyRead.connect(self.handledata)

        format = QtMultimedia.QAudioFormat()
        format.setChannelCount(1)
        format.setSampleRate(96000)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
        format.setSampleType(QtMultimedia.QAudioFormat.UnSignedInt)

        self.audiodevice = QtMultimedia.QAudioDeviceInfo.defaultInputDevice()
        # print self.audiodevice
        # print self.audiodevice.isFormatSupported(format)
        if not self.audiodevice.isFormatSupported(format):
            format = self.audiodevice.nearestFormat(format)

        self.iodevice  = AudioIODevice()

        self.audio = QtMultimedia.QAudioInput(self.audiodevice, format, self)
        self.audio.stateChanged.connect(self.handlestateChange)

    def initUI(self):
        self.startButton = QtGui.QPushButton("start")
        self.pauseButton = QtGui.QPushButton("pause")
        self.stopButton = QtGui.QPushButton("stop")
        mainlayout = QtGui.QHBoxLayout()
        mainlayout.addWidget(self.startButton)
        mainlayout.addWidget(self.pauseButton)
        mainlayout.addWidget(self.stopButton)
        self.setLayout(mainlayout)

        self.startButton.clicked.connect(self.startRecording)
        self.pauseButton.clicked.connect(self.pasueRecording)
        self.stopButton.clicked.connect(self.stopRecording)

    def startRecording(self):
        self.audio.start(self.audiofile)
        # self.audio.start(self.iodevice)

    def pasueRecording(self):
        self.audio.suspend()

    def stopRecording(self):
        self.audio.stop()
        self.audiofile.close()
        # del self.audio

    def handledata(self):
        print '..........'

    def handlestateChange(self, state):
        print state
        # print self.iodevice.readAll()
        # print self.audiofile.flush()

    def closeEvent(self, event):
        self.stopRecording()


def getAvailableDevices():
    devicenames = {}
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
    main = AudioRecord()
    main.show()
    sys.exit(app.exec_())
