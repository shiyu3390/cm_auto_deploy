#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config

reload(sys)
sys.setdefaultencoding('utf-8')
CONFIG = bde_config.get_config()
CLUSTER_HOSTS = CONFIG.get("CDH", "cluster.hosts").strip().split(',')
# JAVA_HOME = CONFIG.get("CM", "java.home").strip()
# if JAVA_HOME == "":
#     JAVA_HOME = "/home/sinorail/jdk1.8.0_121"

HOST_CONFIG = {
    # 'java_home': JAVA_HOME,
    'memory_overcommit_threshold': '0.9',
    'host_health_suppression_host_agent_log_directory_free_space': 'true',
    'host_health_suppression_host_agent_parcel_directory_free_space': 'true',
    'host_config_suppression_parcels_directory': 'true',
    'host_health_suppression_host_agent_process_directory_free_space': 'true',
}


def add_hosts(cluster, api):
    hosts = api.get_all_hosts()
    host_list = hosts.to_json_dict()[hosts.LIST_KEY]
    host_id_dic = {}
    host_ip_dic = {}
    host_ids = list()
    for hostInfo in host_list:
        # hostname = hostInfo['hostname']
        host_id = hostInfo['hostId']
        host_ip = hostInfo['ipAddress']
        host_ids.append(host_id)
        # host_id_dic[hostname] = host_id
        host_id_dic[host_ip] = host_id
        host_ip_dic[host_id] = host_ip
    print "已经成功启动agent的机器信息:", host_list
    # 检查哪些agent没有正常启动
    fail_agent = 0
    for host in CLUSTER_HOSTS:
        if host_id_dic[host] is None:
            fail_agent += 1
            print host, "上的agent没有成功启动,请检查日志/var/log/cloudera-scm-agent/cloudera-scm-agent.log" \
                        "查看报错信息进行修复,最后重启agent,service cloudera-scm-agent restart"
    if fail_agent > 0:
        print "添加机器信息失败，请确保所有机器上的agent都成功启动"
        sys.exit(1)

    for apiHost in hosts:
        apiHost.update_config(HOST_CONFIG)

    if len(cluster.list_hosts()) <= 1:
        cluster.add_hosts(host_ids)

    return cluster, host_id_dic, host_ip_dic
