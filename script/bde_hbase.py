#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config
import bde_zookeeper
import bde_hdfs

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
ALL_HOSTS = CONFIG.get("CDH", "cluster.hosts").strip()
HBASE_HM_HOST = CONFIG.get("HBASE", "hbase.master.hosts").strip()
HBASE_REGIONSERVER_HOST = CONFIG.get("HBASE", "hbase.regionserver.hosts").strip()
if HBASE_REGIONSERVER_HOST == "":
    HBASE_REGIONSERVER_HOST = ALL_HOSTS

HBASE_MASTER_JAVA_HEAPSIZE = CONFIG.get("HBASE", "hbase.master.java.heapsize").strip()
if HBASE_MASTER_JAVA_HEAPSIZE == "":
    HBASE_MASTER_JAVA_HEAPSIZE = 536870912

HBASE_REGIONSERVER_JAVA_HEAPSIZE = CONFIG.get("HBASE", "hbase.regionserver.java.heapsize").strip()
if HBASE_REGIONSERVER_JAVA_HEAPSIZE == "":
    HBASE_REGIONSERVER_JAVA_HEAPSIZE = 2147483648

SERVICE_NAME = "hbase"
HBASE_SERVICE_CONFIG = {
    'hdfs_service': bde_hdfs.SERVICE_NAME,
    'zookeeper_service': bde_zookeeper.SERVICE_NAME,
    'hbase_master_health_enabled': 'false',
    # 'hbase.client.write.buffer': 8388608,
}

HBASE_HM_CONFIG = {
    'hbase_master_java_heapsize': HBASE_MASTER_JAVA_HEAPSIZE,
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_master_log_directory_free_space': 'true',
    'role_health_suppression_master_heap_dump_directory_free_space': 'true',
}

HBASE_RS_CONFIG = {
    # 'hbase_regionserver_regionSplitLimit': 1,
    'hbase_regionserver_wal_pipelines': 4,
    # 'hbase_hregion_memstore_block_multiplier': 4,
    # 'hbase_hstore_blockingStoreFiles': 100,
    'hbase_regionserver_thread_compaction_small': 4,
    # 'hbase_regionserver_handler_count': 100,
    'hbase_regionserver_java_heapsize': HBASE_REGIONSERVER_JAVA_HEAPSIZE,
    # 'hbase_hregion_majorcompaction': 0,
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_region_server_swap_memory_usage': 'true',
    'role_health_suppression_region_server_log_directory_free_space': 'true',
    'role_health_suppression_region_server_heap_dump_directory_free_space': 'true',
    'role_health_suppression_region_server_master_connectivity': 'true',
}


HBASE_GW_CONFIG = {
    'hbase_client_java_heapsize': 1073741824,
}


# Deploys HBase - HMaster, RSes, gateways
def deploy_hbase(cluster, host_id_dic, service_names):
    hbase_service = None
    if not service_names.__contains__(SERVICE_NAME):
        hbase_service = cluster.create_service(SERVICE_NAME, "HBASE")
        hbase_service.update_config(HBASE_SERVICE_CONFIG)

        hm = hbase_service.get_role_config_group("{0}-MASTER-BASE".format(SERVICE_NAME))
        hm.update_config(HBASE_HM_CONFIG)
        master_id_list = list()
        if HBASE_HM_HOST == "":
            master_id_list.append(host_id_dic.values()[0])
            if len(host_id_dic.values()) >= 3:
                master_id_list.append(host_id_dic.values()[len(host_id_dic.values()) - 1])
        else:
            for host in HBASE_HM_HOST.split(","):
                master_id_list.append(host_id_dic[host])

        master_id = 0
        for hm_id in master_id_list:
            master_id += 1
            hbase_service.create_role("{0}-hm-".format(SERVICE_NAME) + str(master_id), "MASTER", hm_id)

        rs = hbase_service.get_role_config_group("{0}-REGIONSERVER-BASE".format(SERVICE_NAME))
        rs.update_config(HBASE_RS_CONFIG)

        gw = hbase_service.get_role_config_group("{0}-GATEWAY-BASE".format(SERVICE_NAME))
        gw.update_config(HBASE_GW_CONFIG)

        regionserver = 0

        for host in HBASE_REGIONSERVER_HOST.split(","):
            regionserver += 1
            hbase_service.create_role("{0}-rs-".format(SERVICE_NAME) + str(regionserver), "REGIONSERVER",
                                      host_id_dic[host])

        gateway = 0
        for host in ALL_HOSTS.split(","):
            gateway += 1
            hbase_service.create_role("{0}-gw-".format(SERVICE_NAME) + str(gateway), "GATEWAY", host_id_dic[host])

        # hbase_service.create_hbase_root()
        cluster.deploy_client_config()
    else:
        hbase_service = cluster.get_service(SERVICE_NAME)

    return hbase_service
