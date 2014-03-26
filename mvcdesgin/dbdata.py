#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os


def getDataByID(dbID):
    data = {
        'app': '11111',
        'mfd': '222222',
        'command': '3333333',
        'subMenu': '4444444',
    }
    return data[dbID]
