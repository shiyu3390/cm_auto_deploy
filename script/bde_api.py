#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config
from cm_api.api_client import ApiResource

reload(sys)
sys.setdefaultencoding('utf-8')
CONFIG = bde_config.get_config()
CM_HOST = CONFIG.get("CM", "cm.host").strip()
CM_PORT = CONFIG.get("CM", "cm.port").strip()
ADMIN_USER = CONFIG.get("CM", "admin.name").strip()
ADMIN_PASS = CONFIG.get("CM", "admin.password").strip()
VERSION = CONFIG.get("CM", "api.version").strip()

CM_CONFIG = {
    'allow_usage_data': 'false',
    'enable_embedded_db_check': 'false',
    'cluster_stats_schedule': 'NEVER',
    'cluster_stats_http': 'false',
    'phone_home': 'false',
    'using_help_from_ccp': 'false',
}


def get_api():
    api = ApiResource(server_host=CM_HOST, server_port=CM_PORT, username=ADMIN_USER, password=ADMIN_PASS,
                      version=VERSION)
    return api


def get_cloudera_manager(api):
    cm = api.get_cloudera_manager()
    cm.update_config(CM_CONFIG)
    print "Connected to CM host on " + CM_HOST + " and updated CM configuration"
    return cm
