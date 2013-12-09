#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

#log write in file
logpath = os.sep.join([os.getcwd(), 'Log', 'main.log'])
fh = RotatingFileHandler(logpath, maxBytes=10 * 1024 * 1024, backupCount=100)
fh.setLevel(logging.DEBUG)

#log write in console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#log formatter
formatter = logging.Formatter('%(asctime)s %(levelname)8s [%(filename)16s:%(lineno)04s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('foorbarfdddddddddddddddddddddddddddddddddddddddddddddddddd')
