#!/usr/bin/env python
# coding=utf-8
import random
import sys
from cm_api.api_client import ApiException
from cm_api.endpoints.services import ApiServiceSetupInfo

import bde_config

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
CM_HOST = CONFIG.get("CM", "cm.host").strip()
DB_TYPE = CONFIG.get("CM", "db.type").strip()
DB_HOST = CONFIG.get("CM", "db.host").strip()
DB_PORT = CONFIG.get("CM", "db.port").strip()
DB_USER = CONFIG.get("CM", "db.user").strip()
DB_PASSWD = CONFIG.get("CM", "db.passwd").strip()

HOSTMONITOR_STORAGE_DIRECTORY = CONFIG.get("CM", "hostmonitor.storage.directory").strip()
SERVICEMONITOR_STORAGE_DIRECTORY = CONFIG.get("CM", "servicemonitor.storage.directory").strip()
EVENTSERVER_INDEX_DIR = CONFIG.get("CM", "eventserver.index.directory").strip()

HOSTMONITOR_HOST = CONFIG.get("CM", "hostmonitor.host").strip()
SERVICEMONITOR_HOST = CONFIG.get("CM", "servicemonitor.host").strip()
ACTIVITYMONITOR_HOST = CONFIG.get("CM", "activitymonitor.host").strip()
EVENTMONITOR_HOST = CONFIG.get("CM", "eventmonitor.host").strip()
ALERTPUBLISHER_HOST = CONFIG.get("CM", "alertpublisher.host").strip()

if EVENTSERVER_INDEX_DIR == "":
    EVENTSERVER_INDEX_DIR = "/var/lib/cloudera-scm-eventserver"
else:
    if EVENTSERVER_INDEX_DIR.endswith("/"):
        EVENTSERVER_INDEX_DIR = EVENTSERVER_INDEX_DIR[0:len(EVENTSERVER_INDEX_DIR) - 1]

    EVENTSERVER_INDEX_DIR += "/eventServerData"

if HOSTMONITOR_STORAGE_DIRECTORY == "":
    HOSTMONITOR_STORAGE_DIRECTORY = "/var/lib/cloudera-host-monitor"
else:
    if HOSTMONITOR_STORAGE_DIRECTORY.endswith("/"):
        HOSTMONITOR_STORAGE_DIRECTORY = HOSTMONITOR_STORAGE_DIRECTORY[0:len(HOSTMONITOR_STORAGE_DIRECTORY) - 1]

    HOSTMONITOR_STORAGE_DIRECTORY += "/hostMonitorData"

if SERVICEMONITOR_STORAGE_DIRECTORY == "":
    SERVICEMONITOR_STORAGE_DIRECTORY = "/var/lib/cloudera-service-monitor"
else:
    if SERVICEMONITOR_STORAGE_DIRECTORY.endswith("/"):
        SERVICEMONITOR_STORAGE_DIRECTORY = SERVICEMONITOR_STORAGE_DIRECTORY[0:len(SERVICEMONITOR_STORAGE_DIRECTORY) - 1]

    SERVICEMONITOR_STORAGE_DIRECTORY += "/serviceMonitorData"

AMON_ROLE_CONFIG = {
    'firehose_database_host': DB_HOST + ":" + DB_PORT,
    'firehose_database_user': DB_USER,
    'firehose_database_password': DB_PASSWD,
    'firehose_database_type': DB_TYPE,
    'firehose_database_name': 'amon',
    'firehose_heapsize': '268435456',
    'max_log_backup_index': '1',
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_activity_monitor_heap_dump_directory_free_space': 'true',
    'role_health_suppression_activity_monitor_log_directory_free_space': 'true',
}
APUB_ROLE_CONFIG = {
    'max_log_backup_index': '1',
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_alert_publisher_heap_dump_directory_free_space': 'true',
    'role_health_suppression_alert_publisher_log_directory_free_space': 'true',
}
ESERV_ROLE_CONFIG = {
    'event_server_heapsize': '268435456',
    'max_log_backup_index': '1',
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'eventserver_index_dir': EVENTSERVER_INDEX_DIR,
    'role_health_suppression_event_server_heap_dump_directory_free_space': 'true',
    'role_health_suppression_event_server_log_directory_free_space': 'true',
}
HMON_ROLE_CONFIG = {
    'max_log_backup_index': '1',
    'firehose_heapsize': '536870912',
    'firehose_non_java_memory_bytes': '1073741824',
    'firehose_storage_dir': HOSTMONITOR_STORAGE_DIRECTORY,
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_host_monitor_heap_dump_directory_free_space': 'true',
    'role_health_suppression_host_monitor_log_directory_free_space': 'true',
    # 'role_config_suppression_firehose_heap_size_validator': 'true',
    # 'role_config_suppression_firehose_non_java_memory_validator': 'true',
}
SMON_ROLE_CONFIG = {
    'max_log_backup_index': '1',
    'firehose_heapsize': '805306368',
    'firehose_non_java_memory_bytes': '1610612736',
    'firehose_storage_dir': SERVICEMONITOR_STORAGE_DIRECTORY,
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_service_monitor_heap_dump_directory_free_space': 'true',
    'role_health_suppression_service_monitor_log_directory_free_space': 'true',
    # 'role_config_suppression_firehose_heap_size_validator': 'true',
    # 'role_config_suppression_firehose_non_java_memory_validator': 'true',
}


def deploy_management(manager, host_id_dic):

    try:
        mgmt = manager.get_service()
    except ApiException:
        print "deploy MGMT service"
        mgmt = None

    if mgmt is None:
        mgmt = manager.create_mgmt_service(ApiServiceSetupInfo(name="MGMT"))
        activitymonitor_host_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if ACTIVITYMONITOR_HOST != "":
            activitymonitor_host_id = host_id_dic[ACTIVITYMONITOR_HOST]

        alertpublisher_host_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if ALERTPUBLISHER_HOST != "":
            alertpublisher_host_id = host_id_dic[ALERTPUBLISHER_HOST]

        eventmonitor_host_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if EVENTMONITOR_HOST != "":
            eventmonitor_host_id = host_id_dic[EVENTMONITOR_HOST]

        hostmonitor_host_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if HOSTMONITOR_HOST != "":
            hostmonitor_host_id = host_id_dic[HOSTMONITOR_HOST]

        servicemonitor_host_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if SERVICEMONITOR_HOST != "":
            servicemonitor_host_id = host_id_dic[SERVICEMONITOR_HOST]

        mgmt.create_role("ActivityMonitor", "ACTIVITYMONITOR", activitymonitor_host_id)
        mgmt.create_role("AlertPublisher", "ALERTPUBLISHER", alertpublisher_host_id)
        mgmt.create_role("EventServer", "EVENTSERVER", eventmonitor_host_id)
        mgmt.create_role("HostMonitor", "HOSTMONITOR", hostmonitor_host_id)
        mgmt.create_role("ServiceMonitor", "SERVICEMONITOR", servicemonitor_host_id)
        # now configure each role
        for group in mgmt.get_all_role_config_groups():
            if group.roleType == "ACTIVITYMONITOR":
                group.update_config(AMON_ROLE_CONFIG)
            elif group.roleType == "ALERTPUBLISHER":
                group.update_config(APUB_ROLE_CONFIG)
            elif group.roleType == "EVENTSERVER":
                group.update_config(ESERV_ROLE_CONFIG)
            elif group.roleType == "HOSTMONITOR":
                group.update_config(HMON_ROLE_CONFIG)
            elif group.roleType == "SERVICEMONITOR":
                group.update_config(SMON_ROLE_CONFIG)

        mgmt.start().wait()

    return mgmt
