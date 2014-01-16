import logging
import os
import time
import sys
from logging.handlers import RotatingFileHandler
from PySide import QtCore


class LogSignal(QtCore.QObject):
    onelogsin = QtCore.Signal(str)
    def __init__(self):
        super(LogSignal, self).__init__()


logSignal = LogSignal()


class LoggerHandler(logging.Handler):
    def __init__(self):
        super(LoggerHandler, self).__init__()
        formatter = logging.Formatter('%(asctime)s %(levelname)8s [%(filename)16s:%(lineno)04s] %(message)s')
        formatter2 = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s')
        self.setFormatter(formatter2)

    def emit(self, record):
        # onemessage = ' '.join([record.asctime, record.levelname, record.module, record.filename, str(record.lineno), record.msg]) 
        # c = "<font color='green'>%s</font>" % onemessage
        onemessage = self.messageFormat(record)
        logSignal.onelogsin.emit(onemessage)

    def messageFormat(self, record):
        levelcolors = {
            'DEBUG': "gray",
            'INFO': "green",
            'WARNING': "orange",
            "ERROR": "red"
        }
        colors = {
        'asctime': 'white',
        'module': "gray",
        "filename": 'white',
        "lineno": "white",
        "msg": "white",
        }

        msgitems = ['asctime', 'levelname', 'module', 'filename', 'lineno', 'msg']
        msglist = []
        for item in msgitems:
            # print colors[item]
            # print getattr(record, msgitems[item])
            if item is "levelname":
                msglist.append("<font color=%s>%s</font>" % (levelcolors[str(getattr(record, item))], str(getattr(record, item))))
            else:
                msglist.append("<font color=%s>%s</font>" % (colors[item], str(getattr(record, item))))
        message = ' '.join(msglist)
        print message
        return message
        # print self.format(record)
        # return self.format(record)


logging.root.setLevel(logging.DEBUG)
logging.root.propagate = 0
#log write in file
logpath = os.sep.join([os.getcwd(), 'Log', 'main.log'])
fh = RotatingFileHandler(logpath, maxBytes=10 * 1024 * 1024, backupCount=100)
fh.setLevel(logging.INFO)
#log write in console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

wh = LoggerHandler()
wh.setLevel(logging.DEBUG)
#log formatter
formatter = logging.Formatter('%(asctime)s %(levelname)8s [%(filename)16s:%(lineno)04s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logging.root.addHandler(fh)
# logging.root.addHandler(ch)
logging.root.addHandler(wh)
logger = logging.root
logger.propagate = 0