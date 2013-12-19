from PySide import QtMultimedia
from PySide import QtCore
from PySide import QtGui
import time
import wave
import json

request = {u'params': {u'bitsPerSample': u'8_BIT', u'audioPassThruDisplayTexts': [{u'fieldText': u'AudioPassThru Display Text 1', u'fieldName': u'audioPassThruDisplayText1'}, {u'fieldText': u'AudioPassThru Display Text 2', u'fieldName': u'audioPassThruDisplayText2'}], u'appID': 65539, u'samplingRate': u'8KHZ', u'audioType': u'PCM', u'maxDuration': 10000}, u'jsonrpc': u'2.0', u'id': 59, u'method': u'UI.PerformAudioPassThru'}

kwargs = request['params']


class AudioRecord(QtGui.QDialog):

    style = '''
        QDialog{
            background-color: rgb(59,67,81);
            color: white;
        }

        QLabel{
            color: white;
            font-size: 30px;
        }
    '''

    def __init__(self, notifyinterval=1, parent=None, **kwargs):
        self.notifyinterval = notifyinterval
        self.parent = parent
        super(AudioRecord, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(300, 200)
        try:
            self.bitsPerSample = int(kwargs['bitsPerSample'].split('_')[0])
            self.samplingRate = int(kwargs['samplingRate'][:-3]) * 1000
            self.audioType = 'audio/%s' % kwargs['audioType'].lower()
            self.maxDuration = kwargs['maxDuration']
            self.textLabels = [i['fieldText'] for i in kwargs['audioPassThruDisplayTexts']]
        except Exception, e:
            print e
            self.bitsPerSample = 8
            self.samplingRate = 8000
            self.audioType = 'audio/pcm'
            self.maxDuration = 10000
            self.textLabels = ['1', '2']

        self.sendbuffer = []
        self.initAudio()
        self.initUI()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(self.maxDuration)
        self.timer.timeout.connect(self.stopAudioRecord)
        self.timer.start()
        self.startRecording()

    def initAudio(self):
        # self.wavfw = wave.open("%s.wav" % time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), 'w')
        self.wavfw = wave.open("record.wav", 'w')
        self.wavfw.setnchannels(1)
        self.wavfw.setsampwidth(self.bitsPerSample / 8)
        self.wavfw.setframerate(self.samplingRate)

        format = QtMultimedia.QAudioFormat()
        format.setChannelCount(1)
        format.setSampleRate(self.samplingRate)
        format.setSampleSize(self.bitsPerSample)
        format.setCodec(self.audioType)
        # format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
        format.setSampleType(QtMultimedia.QAudioFormat.UnSignedInt)

        self.audiodevice = QtMultimedia.QAudioDeviceInfo.defaultInputDevice()
        if not self.audiodevice.isFormatSupported(format):
            format = self.audiodevice.nearestFormat(format)

        self.audio = QtMultimedia.QAudioInput(self.audiodevice, format, self)
        self.audio.setNotifyInterval(self.notifyinterval * 1000)
        self.audio.notify.connect(self.handleNotify)

    def initUI(self):
        self.recordinglabel = QtGui.QLabel("Recording")
        mainlayout = QtGui.QVBoxLayout()
        for text in self.textLabels:
            i = self.textLabels.index(text)
            setattr(self, 'textLabel%d' % i, QtGui.QLabel(text))
            label = getattr(self, 'textLabel%d' % i)
            label.setAlignment(QtCore.Qt.AlignCenter)
            mainlayout.addWidget(label)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)
        self.setStyleSheet(self.style)

    def startRecording(self):
        self.io = self.audio.start()
        self.io.readyRead.connect(self.handleDataReadyRead)

    def pasueRecording(self):
        self.audio.suspend()

    def resumeRecording(self):
        self.audio.resume()

    def stopRecording(self):
        self.audio.stop()

    def handleDataReadyRead(self):
        databuffer = self.io.readAll().data()
        # print type(databuffer)
        self.sendbuffer.append(databuffer)

    def handleNotify(self):
        print len(self.sendbuffer)
        primarydata = ''.join(self.sendbuffer)
        data = primarydata.encode("base64")
        jsondata = json.loads(json.dumps(data)).decode("base64")
        self.wavfw.writeframes(jsondata)
        self.sendbuffer = []

    def stopAudioRecord(self):
        self.stopRecording()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, "dragPosition"):
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


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
    # import sys
    # print getAvailableDevices()
    # app = QtGui.QApplication(sys.argv)
    # main = AudioRecord(notifyinterval=1, **kwargs)
    # main.show()
    # sys.exit(app.exec_())
    data = '''gIB/gICAgH+AgICAgICAgICAgIB/gH+AgICAgH+AgICBgH+AgICAgICAgICAgICAgICAgICAf4CA
f4CAgICAgICAgICBgICAgICAgIGAgICBgYCAgH+BgYCAgICAgICBgICAgYCAgICAf4CAgICAgICA
gIB/f3+AgICAf4CAgICAgICAgIGAgYCAgICAgIF/gIF/gICAgICAgH+AgIB/gH+AgICAgH+AgICA
gIB/gICAgICAgIB/f4CAgICAgYCAgYCAf4CAgICAgICAgIGAgIB/gX+BgICAf3+AgIB/gH+AgIB/
gICAgIGAgIB/gICBgICAgICAgICBgICAgYGAgICAgICAgH+BgICAgICAgIGAgH+AgIB/gICAgYB/
gICAgICAf3+AgH+BgIGAgICAgICBgH+Af4CAf4CAgX9/gICAgICAgICAgICAgICAf4CAgICAf4CA
gICAgICAgYCAgIGAgH9/gICAgX+AgIB/gYCAgIF/gICAgICAgICAgIB/gICAgICAgICAgIF/gIB/
goCAgICAgICAgICAgICAgICAgICAgIB/gICAf4CBf4CAgIGAgIGBgIGAgICBgICAgICBgICAgH+A
gICBgICAgICBgYCAgICAf4B/gICBgICBgICBgICAgX9/gYCAgH+AgICAgICAgIB/gICAf4CAgYB/
gICAgICAgICAf4CAgIGAgICAgH+AgICAf4CAgH+AgICAgH+Af4GAgIGAgICAgICAgH+AgICBgIGA
gICAf4CAgYGAgIB/f4CAgH+AgIGAgYCAgYCAgYCAgICAgICAgICAf4GAgIB/gICAgH+Af4B/gICA
gIB/gICAgICAgICAf4CAgH+BgX+AgICAgICAf4CAgH+Af3+AgICAgH+Af4CAgIB/gH9/gICAgH+A
gH+AgICBgICAgICAgYCAf4CAgYCAgIGBgICAf4CAgICBgIGAgH+AgIB/f4CAgICAgICAgH+AgICA
gICAgICAgIGBgYB/gICAgICAgX9/gICAgICBgH+AgICAgICAgH+AgICAgICAf4CAf4GBgICAgIGA
gICAgICAgICAgICBgICAgICAgYB/gICAgICAgYCBgH+AgICAf4CAgICAgH+AgH9/gIB/gYCAgIB/
gIB/gICAgIB/f3+AgICAgICAgICAgICAgH+Af4CAgICBgICAgICAgICAgICAgYCAgICAgICBgICA
gICAf4CBgICAgICAgIF/gICAgICAgICBgH+AgYCAf4CAgICAgICAgIGAgICAgICAgH+AgICAgICA
gICBgICAgICBgICBgIF/gICBgYCAgICAgH+AgICAgICAgICAgH+Af4CAgICAgH+AgICAgYCAgICA
gIGAgIGAgIGBgICAgICAgICAgIGAgICAgICAgYCAgICAgYCAgICAgIB/gIGAgICAf3+AgIB/gYCA
f4CAgICAgICAgICAgIGAgICBgIGAgICAgICBgYCAf3+AgIGAgICAgYCAgYCAgYCBgICAgICAf4GA
gIGAgIGAgIGBgIB/gIF/gICAgICAgICAgICAgIB/gICAgIGAgICAgICAgICAf4F/gICAgICAgICB
gIGAgICBf4CAgICAgH+AgIB/gICAgIGBgIGAgICAgICAgICAf39/gICAgYCAf4CAgICAf4B/gIGA
gIGAgH+Af4CAgH+AgX+AgICAf4CBgH+BgYCBf4CAgYCAf4GAgIGAgICAgYCAgICBgICAf4CBgIF/
gIGAgH+Af3+AgH+AgICAgICAf4CBgIGAf4CAgYCAgICAgH+Af4CAgICAgICBgIGAgICAgICAgICA
gH+AgICAgICBgICAgIGAgICAgICAgIB/gIGAgICAgICAgICAgICAgICAgYCAgICBgICBgICAf4CA
gICBgYCBgIB/gH+AgICAgICAgICAgICAgYCAgICAgICAgICAgICAgICAgIGAgICBgICAgYCAgICB
gYCAgYCAgICBgYCAf4GAgH+AgICAgIGAgYCAgIGAf4B/gIB/gICAf4CAgICAgICAgX+BgICAf4CA
gICAgYCAgICAgICAgYCAgICAgICAgYCBgH+AgICBgICAgICAgYCAgYGAgICAgICAgICAgIB/gICA
f4B/gICAgICAgH+BgIGAgICAgYCAf4CBf4CAgICAgICAgICAgICBf4CAgICAgIB/gICAgICAgH+A
gYCAgIGAgICAgICAgICAgICAgIGAgYB/f3+AgICAgICAf4CAgYCAgYCAgICAgICAgICAgICAgH+A
gICAgICAf4CAgICAgIGBgYCAgIGAgH+BgH+AgH+AgICAf4CAgICBgICAgYCAgX+AgICAgIB/gIGA
gICBf4CAgH+AgIB/gIGAf4CAf3+AgICAf39/gICAgICAgICAgYB/gIGAgICAgH+AgICAgIB/gYCA
gICBgICAf4CBgICAgICAgICAgH+Bf4CBgICAgICAgICAgICAgICAgYCAgIB/gYCAgICAgIGAgYCA
gH+AgIB/gICBgYCAgIB/gIGAf4CAgIB/gIGAgIB/f4CAgICBgICAgH+AgICBgICAgIGAf4CAf4CA
gICAgICAgICAgYCBgIB/f4CAgICAgICAgICBgX+BgH+AgIB/gICAgIB/gYCAgICAgICAgICAgYCA
f4GBgICAgICAgICAgYCAgICAgICAgH+AgIGAgIGAgICBgIGAgICAgX+AgICBgH+AgIGBgH+AgICA
gYCAgYCAgIGAgICAgIGAgICAgICAgYCAgIB/gIB/f4B/gICAgYGAgIB/gYCAgICBgIGAgIGBgICA
gIB/gICAgICAgYGAgICBgIGAgICAgICAgICAgICAgIGBgIB/gICBgIB/gYCAgIGAgICAgICAgICA
gICBgICAf4GBgYCBgIB/f4CAgICAgYCAgIB/gYCBgYCAgICAgYCAgICAgICAgYB/gICAgICAf4GB
gIGAgICAgICBgYGAgIGAgIB/gICAgICAf3+AgICAgIGAgn+AgICAgICBgICAgICAgIGAgYCAgH9/
gICAgIGAgICAgICBgH+AgICAgIGAgICAgICAgICAgX+AgICAgICAgICAgIB/f4CAgICAgH+AgH9/
gICAgICAgICAgICAgICAgH+AgICAgH+BgICAgICAgICAgH+BgIB/gICAgYB/gICAgICAgIF/gICA
f3+AgICBgICAgICBgH9/gICAgICAgH+Af4CBgICAgIGAgICAgH+AgICAgICAgYCAgICAgH+AgIB/
gICAgICAgIB/gICAgYCBgH+AgYCAf4CAgICAgIGAgYCAgICAgYCBgICAgYCBgICAf4CAgICAgICA
gH+AgICAgICBgICAgICBgICBgICBgICBgICBgICAgICAgICAgICBgIB/gIB/gH+AgIGBgICBf4CA
gICAgIGAgH+AgICAf4CAgICAgIB/gICBgICAgIGAgICAgH+AgICAgIGAgICAgICAgYB/gH+BgICA
gH+Af4CAgIB/gYGAgIGAgICBgYB/gICAgICAgIB/gICAgIF/gIB/gYCAgICBgYCAgH9/gICAgYCA
gICAgIGAgH+AgICAgICAgIGAgH+AgICAgICAgICAgICAgICAgIGAgH+AgH9/f39/gICAgIGAf3+B
f4B/gICAgICAgICAgIGAgICAf4CAgIB/gICAgYCAgIGAgICAgICAgICAgYCAgH+AgH+AgIB/gICA
f4B/gH+BgICAgICBgIGAgICAgICAgICAgIGAgH+AgICAgICAgICAf4CAgYCAf4CAgICAgICAf4CA
gICAgIGAgICAgH+AgH+AgICAgICAgICAgIGBgYGAgH+BgICAgIGAgICAgICAgYCAgYCBgICBgICA
gIF/gICAgIGBgIB/gH9/gICAgYGAf4CAgICAgIGAgX+AgYCAgH+AgICBgH+Af3+AgIGAgICBgICA
gIF/gH+AgICBgICAgH+AgH+AgH9/gICAgIB/gIGAgIB/gICAgIF/gICAf4CAgICAgICAgICAgICA
gICAgICAgICBgICAgICAgIB/gICAgICAgICAf4CBgICAgH+AgIGAgICAgH+AgICAgIB/gIB/gICA
f3+AgIB/gICAgICAgICAgICAgICAf4CAgH+AgIB/gICAgIGAgICAf4GAgICAgIGAgICAgICAgICA
gH+Af4CAgIB/gICAgICAgICAgICAgYCBgICBgICAgICBgICAgICAgIB/gICAf3+AgICAf3+BgICB
gICBgICAf4GAgICAgIB/gICAgICAgIB/gICAgICAgICAgIB/gH+Af4CAgH+Af4B/gYCAgICAf4B/
gH+AgICAf4B/gIGAgICAgICBgICAgICAf4CAgICAgICAgYCBgYCAgICAgYCAgICBgIGAgICAgICA
gICAgICAgYGAgICAf4CAgICAgICAgICAgICAgICAgICAgICAgICAf4CBgICAgICAgH+BgICAgYCB
gICAgICAgH+AgYCAgYGAgICAf4GBgICBgYCAgICAgICAgICAgIGAgICAgIB/f4GAgIGAgH+Af4GA
gYCAgH+Bf4CAgICAgICAgICAgICAf4CAgICBgICAgICAgIB/gICAf4CAgYB/gICAgIGBgYCAf4CA
f4CAgIB/gICBgIGAgYCAgICBgYCAgICAgIB/gX+Af4CAgICAgICAgICAgICAgYCAgICAgICAgICA
gICAf4CAgIGAgICAf4B/gIGAgIGAgICAgICAgICAgX+Bf4CAf4CAgIB/gICAgICBgYCAgICAgH+B
gICAgIB/gICAgICAf4B/gICAgIGAgICAgICAgICAgICBgICAgIGAgICBgICAgICAgH9/gICAgYCA
gIB/gYCAf4CAgYCAgICAgIGAgICAgYCAgIGBgYGAgICAgYGBgICAgYCAgH+BgYB/gICAgICAgICA
gICBgIGAgICAgICBgYCBf4CAgIB/gIGAgICAgICAgICAgICAgICAgICAgYCAgICAgICAgYCAgICA
gICAgIB/gICBgICAgICAgICAgICAgICAgICAgIF/gICAgICAgIGAgICAgH+AgICAgICAgICAf39/
f4B/gICAgICAf3+Af4CAgH+AgICAgICAgYCAgICAgICAgICBgYCAgICAgICAgICAgYCAgICAgYGA
gIB/gH+AgICAf4CAgICBf4CAgYCAgICBgYCAgH+AgIB/gICAgIGAf4CAgICAgICAgICAgYCAgYCA
gIGAgIB/f4CAgICAgICAgIGAgIB/f4CAgICAgICAgIB/gICAgIB/gICAf4CBgICAgH+Af3+AgICA
gYCAgICAgYCAgYGAgX+AgICAgICAgICAgICBgICAgICAgH+AgICAgICAf4GAgYCAgYCAgICAgX+A
gICAgIGAgH+AgIB/gYCAgX9/gICAgICAgICAgYCAgICAgYCAgICBgH9/gICAf4CAgICAf4CAgIB/
gICAgICAgICAgICAgIB/gICAgICAgICAgYCAgICAgICAgICBgICAgICAgICAgICAgICAgICAgICA
gICAgYB/gICAgICBgICAgYGAgIB/gYGAgICAgICAgICAgICAgICAgH+AgICAgICAgICAf39/gICA
gICAgICAgICAgICBgIF/gICAgICAf4CBf4CAgICAgIB/gICAf4B/gICAgIB/gICAgICAf4CAgICA
f4CAf3+AgICAgIGAgICAgH+AgICAgICAgICAgIGAgIF/gYCAgH9/gICAf4B/gICAgICAgICBgICA
gICAgYCBgICAgICAgYCAgIGBgICAgICAgICAgYCAgICAgICBgICAgYCAf4CAgIGAf4CAgICAgH9/
gIB/gYCBgICAgICAgYCAgICAgICAgIF/gICAgICAgICAgYCAgICAgICAgICAgICAgICAgYCAgIGA
gICBgICAf4CAgIF/gICAf4GAgICBgICAgICAgICAgICAf4CAgICAgICAgICAf4CAf4GAf3+AgICA
gICAgICAf3+AgICAgICAf4CAgH+AgH9/gICAgICBgX+AgICAgICAgICAgYCAgIB/gICAgYCAgICA
gIGAgICAgH+Af4GAgICAgICAgYCAgIB/f4GAgIB/gICAgICAgICAf4CAgH+AgIGBgICAgICAgICA
gH+BgICBgICAgIF/gYCAgH+AgIB/f4CAgH9/gH+BgICBgICAgICAgYB/gICAgYCAgH+AgH+AgIGA
gICAf3+AgIB/gICBgIGAgIGAgIGAgICAgICAgICAgICBgICAf4CAgIB/gX+Af4CAgICAf4CAgIGA
gICAgICAgIB/gYF/gICAgICAgH+AgICAgH9/gICAgIB/gH+AgICAf4B/gICAgIB/gIB/gICAgYCA
gICAgIGAgICAgIGAgICBgYCAgICAgICAgYGBgIB/gICAf3+AgICAgICAgIB/gIB/gICAgICAgICB
gICAf4CAgICAgIF/f4CAgICAgYB/gICAgICAgH9/gICAgIGAgICAgH+BgYCAgICBgICAgICAgICA
gICAgYCAgICAgIGAgICAgICAgIGAgYB/f4CAgH+AgICAgIB/gIB/gICAf4GAgICAgICAf4CAgICA
f4B/gICAgICAgICAgICAgIB/gH+AgICAgYCAgICAgICAgH+AgIGAgICAgICAgYCAgICAgH+AgYCA
gICAgICAf4CAf4CAgICAgYB/gIGAgH+AgICAf4CAgICBgICAgICAgIB/gICAgICAgICAgYB/gICA
gYCAgICBf4CAgICAgICAf4B/f4CAgICAgICAgIB/gH+AgICAgIB/f4CAgICAgICAgICAgICAgICB
gYB/gICAf4CAgICAgICAgICAgICAgICAgIGAgICAgICAf3+AgICAgH+AgICAf4GAgH+AgICAgICA
gICAgICAgICAgYCAf4CAgICAgIGAgH9/gICAgH+AgIGAgIGAgIGAgYCAgICAgH+AgICAgICBgICA
gICAf3+Af4CAgICAgICAgICAgICAf4CAgICBgICAgICAgICAgH+Bf4CAgICAgICAgYCBgICAgX+A
gICAgICAgICAf4CAgICBgICBgICAgICAgICAgH9/f3+AgICAgH+AgICAgH+Af4CBgICBgIB/gH+A
gIB/gIF/gICAgH+AgYB/gYGAgX+AgIGAgH+BgICBgICAgIGAgICAgYB/gH+AgYCBf4CBgICAgICA
gICAgICAgICAgH+AgYCBgH+AgIGAgICAgIB/gICAgICAgICAgYCBgICAgICAgICAgIB/gICAgICA
gYCAgICBgICAgICAgICAf4CBgICAgICAgICAgICAgICAf4GAgIB/gICAgYCAgH+AgICAgYGAgYCA
f4B/gICAgH+AgICAgICAgICAgICAgICAgICAgICAgICAgICBgICAgYCAgICAgICAgYGAgICAf4CA
gIGAgH+BgH9/gH+AgICBgIB/gICAgH+Af4CAf4CAgH9/gICAgICAgIB/gICAgH+AgICAgIGAgICA
gICAgICAgICAgIB/gICAgYB/gICAgH9/gH+AgIGAgICBgICAgICAgICAgICAf3+AgH9/f4CAgICA
gIB/gX+AgICAgIGAgH+AgH+AgICAgIB/gICAgICAgX+AgICAgICAf4B/gICAgIB/gIGAgICBgICA
gICAgICAgICAgICBgIGAf39/gICAgICAgH+AgIF/gIGAgICAgICAf4CAgIB/gICAgH+AgICAgH+A
gIB/gICAgIGAgICBgIB/gYB/gIB/gICAgH+AgICAgX+AgICAgIB/f4CAgICAf4CAgICAgX+AgH9/
gIB/f4CBgH+AgH9/gICAgH9/f4CAgICAgICAgIGAgICBgICAgIB/gICAgIB/f4GAgICAgIB/gH+A
gH+AgICAgIB/gIB/gH+AgYCAgICAgIB/gICAgICAgIGAgICAf4GAf4B/gICAf4CAgIB/gIB/f4CA
gYGAgICAf4CBgH+AgICAf4CAgICAf3+AgIB/gYCAgIB/gICAgICAgICBgH+AgH+AgICAgICAgICA
gIGAgICAf3+Af4CAgH+AgICAgYF/gIB/f4CAf4CAf4CAf4F/gIB/gICAgICAgIGAgH+BgYCAgICA
gICAgIGAgICAgIB/gIB/gICBgICBgICAgYCBgICAgIF/gICAgYB/gICAgIB/gICAgIGAgIGAgICB
gICAgICBgICAgICAgIGAgICAf4CAf3+Af4CAgIGBgICAf4GAgYCAgYCBgICBgYCAgICAf4CAgICA
gIGAgICAgYCBgICAgH+AgICAgH+AgICAgICAf4CAgICAf4GAgH+Af4B/gICAgICAgICAgICAgH+A
gICAgX+Af3+AgICAgICAgICAf4GAgYGAgICAgIGAgICAgICAgIGAf4CAgICAgH+BgYCBgICAgICA
gYGAgICAgICAf4CAgICAgH9/gICAgICBgIF/gIB/gICAgYCAgICAgICBgIGAgIB/f4CAgICBgH+A
gICAgYB/gICAgICBgICAgICAgICAgIGAgICAgICAgICAgICAgH+AgH+AgIB/gIB/gICAgICAgICA
gICAgICAgIB/gICBgIB/gYCAgICAgICAgIB/gYCAf4CAgIGAf4CAgICAgICBf4B/f39/gICAgYB/
gICAgIB/f4CAgICAgIB/gH9/gICAgICBgICAgIB/f4CAgIB/gIGAgICAgIB/gICAf4CAgICAgICA
f4CAgIGAgYB/gIGAgH+AgICAgICBgIGAgICAgIGAgYCAgIGAgYCAgH+AgICAgICAgIB/gICAgICA
gYCAgIGAgYCAgYCAgYCAgYCAgYCAgICAgICAgICAgYCAgICAf4B/gICBgYCAgX+AgICAgICBgIB/
gICAgH+AgYCAgICAf4CAgICAgICBgICAgIB/gICAgICBgICAgICAgIGAf4B/gYCAgIB/gICAgICA
f4GBgICBgH+AgYGAf4CAgICAgICAf4CAgICBgICAf4CAgICAgIGAgIB/f4CAgIGAgICAgICBgIB/
gICBgICAgICBgICAgICAgICAgICBgICAgICAgICBgICAgICAf4CAgICBgIGBgICAgX+AgICAgIGA
gICAgIGBgICAgYCAgICAf4CAgIGAgICBgICAgICAgICAgIGAgYB/gYF/gICAf4CAgH+Af4F/gYCA
gICAgYCBgICAgICAgICAgICBgIB/gICAgICAgIGBgH+AgIGAgH+AgICAgIGAgH+AgYCAgICBgYCA
gIGAgIB/gICAgICBgYCAgICBgYGBgIB/gYCAgICBgICAgICAgIGAgIGAgYCAgYCAgICBgICAgICB
gYCBgIB/f4CAgIGBgICAgYCAgYCBgIF/gIGAgIB/gICAgYB/gICAgICBgICAgYGAgIGBf4B/gICA
gYCAgICAgIGAgIB/f4GAgICAf4CBgICAf4GAgYCAf4CAgH+AgICAgICAgICAgICAgYCAgIGAgICA
gYCAgICAgICAf4CAgICAgICAgICAgYCAgIB/gICBgICAgIB/gICAgICAf4CAf4CAgH+AgICAf4CA
gICAgICAgICAgICAgH+AgIB/gICAf4CAgICBgICAgH+BgICAgICBgICAgICAgX+AgIB/gH+AgIB/
gICAgICAgICAgICAgIGAgYCAgYCAgICAgYCBgICAgYCAf4CAgH9/gICAgH9/gYCAgYCAgYCAgH+B
gYCAgICAf4CAgICAgICAgICAgICAgICAgICAf4B/gICAgIB/gH+Af4GAgICAgH+Af4B/gICAgH+A
f4CBgICAgICAgYCAgICAgH+AgICAgICAgIGAgYGAgICAgICAgICAgICBgH+AgICAgICAgICAf4GB
gICAgH+AgICAgICAgICAgH+Af4CAf4CAgICAgICAgH+AgYCAgICAf4B/gYCAgIGAgYCAgICAgIB/
gIGAgICBgICAgH+BgICAgYCAgICAgICAgICAgICBgICAgICAf3+BgICBgIB/gH+BgIGAgICAgX+A
gICAgICAgICAgICAgH+AgICAgX+AgICAgICAf4CAgH+AgIGAf4CAgICBgYGAgH+AgH+AgICAf4CA
gICAgIGAgICAgIGAgICAgICAf4B/gH+AgICAgICAgICAgICAgIGAgICAgICAgICAgICAgH+AgICB
gICAgH+Af4CBgICBgICAgICAgICAgIF/gH+AgH+AgICBf4CAgICAgYGAgICAgIB/gICAgICAf4CA
gICAgH+Af4B/gICBgICAgICAf4CAgICAgYCAgICBgH+AgYCAgICAgIB/f4CAgIGAgICAf4CAgH+A
gIGAgICAgICBgICAgIGAgICBgYGAgICAgIGAgYCAgIGAgIB/gYGAf4CAgICAgICAgICAgYCBgICA
gICAgYGAgX+AgICAgICBgICAgICAgICBgICAgICAgICAgIGAgIGAgICAgIGAgICAgICAgICAf4CA
gYCAgICAgICAgICAgICAgICAgICBf4CAgICAgH+BgICAgIB/gICAgICAgICAgH9/f3+Af4CAgICA
gH9/gH+AgIB/gICAgICAgIGAgICAgICAgICAgYGAgICAgICAgICAgIGAgICAgIGBgICAf4B/gICA
gH+AgYCAgX+AgIGAgICAgYGAgIA='''
    d = ''.join(data.split('\n'))
    with open('data.txt', 'w') as f:
        f.write(d)
