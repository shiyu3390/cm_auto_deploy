#!/usr/bin/env python
# coding=utf-8
import sys
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')


def get_config():
    config = ConfigParser.ConfigParser()
    config.read("../config/clouderaconfig.ini")
    return config
