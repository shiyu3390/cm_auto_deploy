#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()

ZOOKEEPER_HOSTS = CONFIG.get("ZOOKEEPER", "zookeeper.hosts").strip()
data_dir = CONFIG.get("ZOOKEEPER", "zookeeper.dataDir").strip()

ZOOKEEPER_DATA_DIR = "/var/lib/zookeeper"
if data_dir != "":
    if data_dir.endswith("/"):
        data_dir = data_dir[0:len(data_dir) - 1]
    ZOOKEEPER_DATA_DIR = data_dir + "/zkData"

zk_java_heapsize = CONFIG.get("ZOOKEEPER", "zookeeper.server.java.heapsize").strip()
ZOOKEEPER_SERVER_JAVA_HEAPSIZE = "536870912"
if zk_java_heapsize != "":
    ZOOKEEPER_SERVER_JAVA_HEAPSIZE = zk_java_heapsize

SERVICE_NAME = "zookeeper"
ZOOKEEPER_SERVICE_CONFIG = {
    'zookeeper_datadir_autocreate': 'true',
    'zookeeper_canary_health_enabled': 'false',
    'tickTime': '6000',
}
ZOOKEEPER_ROLE_CONFIG = {
    'dataLogDir': ZOOKEEPER_DATA_DIR,
    'dataDir': ZOOKEEPER_DATA_DIR,
    'maxSessionTimeout': '60000',
    'minSessionTimeout': '40000',
    'max_log_backup_index': '1',
    'zookeeper_server_java_heapsize': ZOOKEEPER_SERVER_JAVA_HEAPSIZE,
    'oom_sigkill_enabled': 'false',
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_zookeeper_server_swap_memory_usage': 'true',
    'role_health_suppression_zookeeper_server_log_directory_free_space': 'true',
    'role_health_suppression_zookeeper_server_heap_dump_directory_free_space': 'true',
    'role_health_suppression_zookeeper_server_data_log_directory_free_space': 'true',
}


# Deploys and initializes ZooKeeper
def deploy_zookeeper(cluster, host_id_dic, service_names):
    # if platform.system() == 'Linux':
    #     if not os.path.exists(ZOOKEEPER_DATA_DIR):
    #         os.makedirs(ZOOKEEPER_DATA_DIR)
    #     os.system("chown -R zookeeper:zookeeper " + ZOOKEEPER_DATA_DIR)

    zk = None
    if not service_names.__contains__(SERVICE_NAME):
        zk = cluster.create_service(SERVICE_NAME, "ZOOKEEPER")
        zk.update_config(ZOOKEEPER_SERVICE_CONFIG)
        zk_hosts = list()
        host_id_list = host_id_dic.values()
        if ZOOKEEPER_HOSTS == "":
            if len(host_id_dic) <= 2:
                zk_hosts.append(host_id_list[0])
            elif 5 >= len(host_id_dic) >= 3:
                zk_hosts.append(host_id_list[0])
                zk_hosts.append(host_id_list[1])
                zk_hosts.append(host_id_list[2])
            elif len(host_id_dic) > 5:
                zk_hosts.append(host_id_list[0])
                zk_hosts.append(host_id_list[1])
                zk_hosts.append(host_id_list[2])
                zk_hosts.append(host_id_list[3])
                zk_hosts.append(host_id_list[4])
        else:
            for host in ZOOKEEPER_HOSTS.split(","):
                zk_hosts.append(host_id_dic[host])

        zk_id = 0
        for zk_host in zk_hosts:
            zk_id += 1
            ZOOKEEPER_ROLE_CONFIG['serverId'] = zk_id
            role = zk.create_role(SERVICE_NAME + "-" + str(zk_id), "SERVER", zk_host)
            role.update_config(ZOOKEEPER_ROLE_CONFIG)

        zk.init_zookeeper()
        cluster.deploy_client_config()
    else:
        zk = cluster.get_service(SERVICE_NAME)

    return zk
