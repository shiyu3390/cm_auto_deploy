#!/usr/bin/env python
# coding=utf-8
import random
import sys
import bde_config
import bde_hdfs
import bde_zookeeper

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()

### YARN ###
SERVICE_NAME = "yarn"
ALL_HOSTS = CONFIG.get("CDH", "cluster.hosts").strip()
ENABLE_HA = CONFIG.get("YARN", "yarn.ha.enable").strip()
if ENABLE_HA == "":
    ENABLE_HA = "true"

YARN_RM_HOST = CONFIG.get("YARN", "yarn.rm.host").strip()
YARN_BAK_RM_HOST = CONFIG.get("YARN", "yarn.rm.bak.host").strip()

YARN_JHS_HOST = CONFIG.get("YARN", "yarn.jhs.host").strip()
YARN_NM_HOSTS = CONFIG.get("YARN", "yarn.nm.hosts").strip()
if YARN_NM_HOSTS == "":
    YARN_NM_HOSTS = ALL_HOSTS

YARN_NODEMANAGER_RESOURCE_MEMORY_MB = CONFIG.get("YARN", "yarn.nodemanager.resource.memory.mb").strip()
if YARN_NODEMANAGER_RESOURCE_MEMORY_MB is None or YARN_NODEMANAGER_RESOURCE_MEMORY_MB == "":
    YARN_NODEMANAGER_RESOURCE_MEMORY_MB = 10240

yarn_data_dirs = CONFIG.get("YARN", "yarn.data.dirs").strip()
YARN_DATA_DIRS = ""
if yarn_data_dirs == "":
    YARN_DATA_DIRS = '/yarnData,'
else:
    for data_dir in yarn_data_dirs.split(","):
        if data_dir.endswith("/"):
            data_dir = data_dir[0:len(data_dir) - 1]
        YARN_DATA_DIRS += data_dir + '/yarnData,'

YARN_NODEMANAGER_LOCAL_DIRS = ""
YARN_NODEMANAGER_LOG_DIRS = ""
for data_dir in YARN_DATA_DIRS[0:len(YARN_DATA_DIRS) - 1].split(","):
    YARN_NODEMANAGER_LOCAL_DIRS += data_dir + "/nm,"
    YARN_NODEMANAGER_LOG_DIRS += data_dir + "/container-logs,"

YARN_SERVICE_CONFIG = {
    'hdfs_service': bde_hdfs.SERVICE_NAME,
    'zookeeper_service': bde_zookeeper.SERVICE_NAME,
}

YARN_JHS_CONFIG = {
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_jobhistory_log_directory_free_space': 'true',
    'role_health_suppression_jobhistory_heap_dump_directory_free_space': 'true',
    'role_health_suppression_jobhistory_swap_memory_usage': 'true',
}

YARN_RM_CONFIG = {
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'yarn_resourcemanager_max_completed_applications': 100,
    'yarn_scheduler_minimum_allocation_mb': 128,
    'yarn_resourcemanager_recovery_enabled': 'true',
    'yarn_resourcemanager_am_max_retries': 3,
    'yarn_scheduler_increment_allocation_mb': 128,
    'yarn_scheduler_fair_continuous_scheduling_enabled': 'true',
    'yarn_resourcemanager_nm_liveness_monitor_interval_ms': 10000,
    'yarn_resourcemanager_amliveliness_monitor_interval_ms': 10000,
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_resource_manager_swap_memory_usage': 'true',
    'role_health_suppression_resource_manager_log_directory_free_space': 'true',
    'role_health_suppression_resource_manager_heap_dump_directory_free_space': 'true',
}
YARN_NM_CONFIG = {
    'yarn_nodemanager_resource_cpu_vcores': 32,
    'yarn_nodemanager_resource_memory_mb': YARN_NODEMANAGER_RESOURCE_MEMORY_MB,
    'yarn_nodemanager_local_dirs': YARN_NODEMANAGER_LOCAL_DIRS[0:len(YARN_NODEMANAGER_LOCAL_DIRS) - 1],
    'yarn_nodemanager_log_dirs': YARN_NODEMANAGER_LOG_DIRS[0:len(YARN_NODEMANAGER_LOG_DIRS) - 1],
    'yarn_nodemanager_recovery_dir': YARN_DATA_DIRS.split(",")[0] + '/yarn-nm-recovery',
    'nodemanager_config_safety_valve': '<property><name>yarn.nodemanager.vmem-pmem-ratio</name><value>3.1</value></property><property><name>yarn.nodemanager.vmem-check-enabled</name><value>false</value></property><property><name>yarn.nodemanager.pmem-check-enabled</name><value>false</value></property>',
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_node_manager_swap_memory_usage': 'true',
    'role_health_suppression_node_manager_log_directory_free_space': 'true',
    'role_health_suppression_node_manager_heap_dump_directory_free_space': 'true',
    'nodemanager_connectivity_health_enabled': 'false',
}

YARN_GW_CONFIG = {
    'mapred_submit_replication': min(3, len(YARN_NM_HOSTS.split(","))),
    'mapred_reduce_tasks': 48,
    'mapreduce_map_memory_mb': 1024,
    'mapreduce_map_java_opts_max_heap': 859832320,
    'mapreduce_reduce_memory_mb': 2048,
    'mapreduce_reduce_java_opts_max_heap': 1719664640,
    'yarn_app_mapreduce_am_resource_mb': 1024,
    'yarn_app_mapreduce_am_max_heap': 859832320,
    'mapreduce_client_java_heapsize': 536870912,
    'mapreduce_am_max_attempts': 3,
    'mapred_reduce_tasks_speculative_execution': 'true',
    'mapred_map_tasks_speculative_execution': 'true',
    'mapreduce_reduce_cpu_vcores': 2,
    'mapreduce_job_ubertask_enabled': 'true',
    'mapreduce_job_ubertask_maxbytes': 268435456,
    'mapreduce_client_env_safety_valve': 'HADOOP_CLASSPATH=$HADOOP_CLASSPATH:/opt/cloudera/parcels/CDH/lib/hbase/lib/*',
}


# Deploys YARN - RM, JobHistoryServer, NMs, gateways
# This shouldn't be run if MapReduce is deployed.
def deploy_yarn(cluster, host_id_dic, service_names):
    yarn_service = None
    if not service_names.__contains__(SERVICE_NAME):
        yarn_service = cluster.create_service(SERVICE_NAME, "YARN")
        yarn_service.update_config(YARN_SERVICE_CONFIG)

        rm = yarn_service.get_role_config_group("{0}-RESOURCEMANAGER-BASE".format(SERVICE_NAME))
        rm.update_config(YARN_RM_CONFIG)

        rm_id = host_id_dic.values()[1]
        if YARN_RM_HOST != "":
            rm_id = host_id_dic[YARN_RM_HOST]

        yarn_service.create_role("{0}-rm".format(SERVICE_NAME), "RESOURCEMANAGER", rm_id)

        jhs = yarn_service.get_role_config_group("{0}-JOBHISTORY-BASE".format(SERVICE_NAME))
        jhs.update_config(YARN_JHS_CONFIG)
        jhs_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if YARN_JHS_HOST != "":
            jhs_id = host_id_dic[YARN_JHS_HOST]

        yarn_service.create_role("{0}-jhs".format(SERVICE_NAME), "JOBHISTORY", jhs_id)

        nm = yarn_service.get_role_config_group("{0}-NODEMANAGER-BASE".format(SERVICE_NAME))
        nm.update_config(YARN_NM_CONFIG)

        nodemanager = 0
        for host in YARN_NM_HOSTS.split(","):
            nodemanager += 1
            yarn_service.create_role("{0}-nm-".format(SERVICE_NAME) + str(nodemanager), "NODEMANAGER",
                                     host_id_dic[host])

        gw = yarn_service.get_role_config_group("{0}-GATEWAY-BASE".format(SERVICE_NAME))
        gw.update_config(YARN_GW_CONFIG)

        gateway = 0
        for host in ALL_HOSTS.split(","):
            gateway += 1
            yarn_service.create_role("{0}-gw-".format(SERVICE_NAME) + str(gateway), "GATEWAY", host_id_dic[host])

        if ENABLE_HA == "true":
            new_rm_host_id = host_id_dic.values()[len(host_id_dic.values()) - 1]
            if YARN_BAK_RM_HOST != "":
                new_rm_host_id = host_id_dic[YARN_BAK_RM_HOST]
            yarn_service.enable_rm_ha(new_rm_host_id)

        cluster.deploy_client_config()
    else:
        yarn_service = cluster.get_service(SERVICE_NAME)

    return yarn_service
