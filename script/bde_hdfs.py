#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config
import bde_zookeeper

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
HDFS_NAMESERVICE = CONFIG.get("HDFS", "hdfs.nameservices").strip()
if HDFS_NAMESERVICE == "":
    HDFS_NAMESERVICE = 'sinorail'

ALL_HOSTS = CONFIG.get("CDH", "cluster.hosts").strip()
NN_HOSTS = CONFIG.get("HDFS", "namenode.host").strip()
SNN_HOSTS = CONFIG.get("HDFS", "secondary.host").strip()
DN_HOSTS = CONFIG.get("HDFS", "datanode.hosts").strip()
if DN_HOSTS == "":
    DN_HOSTS = ALL_HOSTS
JN_HOSTS = CONFIG.get("HDFS", "journalnode.hosts").strip()
ENABLE_NN_HA = CONFIG.get("HDFS", "hdfs.ha.enable").strip()

if ENABLE_NN_HA == "":
    ENABLE_NN_HA = "true"

nn_dir = CONFIG.get("HDFS", "namenode.data.dirs").strip()
snn_dir = CONFIG.get("HDFS", "secondary.data.dirs").strip()
dn_dir = CONFIG.get("HDFS", "datanode.data.dirs").strip()
jn_dir = CONFIG.get("HDFS", "journalnode.data.dir").strip()
DFS_NAME_DIR_LIST = ''
base_name_dir = '/nnData,'
if nn_dir == "":
    DFS_NAME_DIR_LIST = '/dfs' + base_name_dir
else:
    for base_dir in nn_dir.split(","):
        if base_dir.endswith("/"):
            base_dir = base_dir[0:len(base_dir) - 1]
        # if (not os.path.exists(base_dir)) and platform.system() == 'Linux':
        #     os.makedirs(base_dir)
        name_dir = base_dir + base_name_dir
        DFS_NAME_DIR_LIST = DFS_NAME_DIR_LIST + name_dir

FS_CHECKPOINT_DIR_LIST = ''
base_snn_dir = '/snnData,'
if snn_dir == "":
    FS_CHECKPOINT_DIR_LIST = '/dfs' + base_snn_dir
else:
    for base_dir in snn_dir.split(","):
        if base_dir.endswith("/"):
            base_dir = base_dir[0:len(base_dir) - 1]
        # if (not os.path.exists(base_dir)) and platform.system() == 'Linux':
        #     os.makedirs(base_dir)
        check_dir = base_dir + base_snn_dir
        FS_CHECKPOINT_DIR_LIST = FS_CHECKPOINT_DIR_LIST + check_dir

DFS_DATA_DIR_LIST = ''
base_data_dir = '/dnData,'
if dn_dir == "":
    DFS_DATA_DIR_LIST = '/dfs' + base_data_dir
else:
    for base_dir in dn_dir.split(","):
        if base_dir.endswith("/"):
            base_dir = base_dir[0:len(base_dir) - 1]
        # if (not os.path.exists(base_dir)) and platform.system() == 'Linux':
        #     os.makedirs(base_dir)
        data_dir = base_dir + base_data_dir
        DFS_DATA_DIR_LIST = DFS_DATA_DIR_LIST + data_dir

DFS_JOURNALNODE_EDITS_DIR = ''
base_jnn_dir = '/jnnData'
if jn_dir == "":
    DFS_JOURNALNODE_EDITS_DIR = '/dfs' + base_jnn_dir
else:
    if jn_dir.endswith("/"):
        jn_dir = jn_dir[0:len(jn_dir) - 1]
    # if (not os.path.exists(jn_dir)) and platform.system() == 'Linux':
    #     os.makedirs(jn_dir)
    DFS_JOURNALNODE_EDITS_DIR = jn_dir + base_jnn_dir

SERVICE_NAME = "hdfs"
HDFS_SERVICE_CONFIG = {
    'dfs_replication': 2,
    'dfs_permissions': 'false',
    'dfs_block_local_path_access_user': 'impala,hbase,mapred,spark,yarn',
    'zookeeper_service': bde_zookeeper.SERVICE_NAME,
    'hdfs_canary_health_enabled': 'false',
    'hdfs_service_config_safety_valve': '<property><name>dfs.namenode.block-placement-policy.default.prefer-local-node</name><value>false</value></property><property><name>dfs.permissions</name><value>false</value></property>'
}
HDFS_NAMENODE_SERVICE_NAME = "nn"
HDFS_NAMENODE_HOST = NN_HOSTS
HDFS_NAMENODE_CONFIG = {
    'dfs_name_dir_list': DFS_NAME_DIR_LIST[0:len(DFS_NAME_DIR_LIST) - 1],
    'max_log_backup_index': 1,
    'oom_sigkill_enabled': 'false',
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_name_node_swap_memory_usage': 'true',
    'role_health_suppression_name_node_log_directory_free_space': 'true',
    'role_health_suppression_name_node_heap_dump_directory_free_space': 'true',
    'role_health_suppression_name_node_data_directories_free_space': 'true',
    'role_config_suppression_namenode_java_heapsize_minimum_validator': 'true',
}
HDFS_SECONDARY_NAMENODE_HOST = SNN_HOSTS
HDFS_SECONDARY_NAMENODE_CONFIG = {
    'fs_checkpoint_dir_list': FS_CHECKPOINT_DIR_LIST[0:len(FS_CHECKPOINT_DIR_LIST) - 1],
    'max_log_backup_index': 1,
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
}
HDFS_DATANODE_HOSTS = DN_HOSTS
HDFS_DATANODE_CONFIG = {
    'dfs_data_dir_list': DFS_DATA_DIR_LIST[0:len(DFS_DATA_DIR_LIST) - 1],
    'datanode_java_heapsize': 1073741824,
    'dfs_datanode_handler_count': 32,
    'dfs_datanode_du_reserved': 1073741824,
    'dfs_datanode_max_xcievers': 8192,
    'dfs_datanode_failed_volumes_tolerated': (len(DFS_DATA_DIR_LIST.split(",")) - 1) / 2,
    'oom_sigkill_enabled': 'false',
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_data_node_swap_memory_usage': 'true',
    'role_health_suppression_data_node_log_directory_free_space': 'true',
    'role_health_suppression_data_node_heap_dump_directory_free_space': 'true',
    'datanode_connectivity_health_enabled': 'false',
    'role_health_suppression_data_node_ha_connectivity': 'true',
}

HDFS_FAILOVER_CONFIG = {
    'oom_sigkill_enabled': 'false',
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_heap_dump_dir': '/tmp',
    'oom_sigkill_enabled': 'false',
    'role_health_suppression_hdfs_failovercontroller_swap_memory_usage': 'true',
    'role_health_suppression_hdfs_failovercontroller_log_directory_free_space': 'true',
    'role_health_suppression_hdfs_failovercontroller_heap_dump_directory_free_space': 'true',
}

HDFS_GATEWAY_HOSTS = ALL_HOSTS
HDFS_GATEWAY_CONFIG = {
    'dfs_client_use_trash': 'true',
    'hdfs_client_env_safety_valve': 'HADOOP_CLASSPATH=$HADOOP_CLASSPATH:/opt/cloudera/parcels/CDH/lib/hbase/lib/*',
}

HDFS_JOURNALNODE_CONFIG = {
    'role_health_suppression_journal_node_heap_dump_directory_free_space': 'true',
    'role_health_suppression_journal_node_edits_directory_free_space': 'true',
    'role_health_suppression_journal_node_log_directory_free_space': 'true',
    'process_auto_restart': 'true',
    'max_log_backup_index': 1,
}

ACTIVE_NAME = ("{0}-" + HDFS_NAMENODE_SERVICE_NAME).format(SERVICE_NAME)


# Deploys HDFS - NN, DNs, SNN, gateways.
def deploy_hdfs(cluster, host_id_dic, service_names):
    hdfs_service = None
    if not service_names.__contains__(SERVICE_NAME):
        hdfs_service = cluster.create_service(SERVICE_NAME, "HDFS")
        hdfs_service.update_config(HDFS_SERVICE_CONFIG)

        nn_role_group = hdfs_service.get_role_config_group("{0}-NAMENODE-BASE".format(SERVICE_NAME))
        nn_role_group.update_config(HDFS_NAMENODE_CONFIG)
        nn_host_id = host_id_dic.values()[0]
        if HDFS_NAMENODE_HOST != "":
            nn_host_id = host_id_dic[HDFS_NAMENODE_HOST]

        hdfs_service.create_role(ACTIVE_NAME, "NAMENODE", nn_host_id)

        failover_role_group = hdfs_service.get_role_config_group("{0}-FAILOVERCONTROLLER-BASE".format(SERVICE_NAME))
        failover_role_group.update_config(HDFS_FAILOVER_CONFIG)

        snn_role_group = hdfs_service.get_role_config_group("{0}-SECONDARYNAMENODE-BASE".format(SERVICE_NAME))
        snn_role_group.update_config(HDFS_SECONDARY_NAMENODE_CONFIG)

        if HDFS_SECONDARY_NAMENODE_HOST != "":
            snn_host_id = host_id_dic[HDFS_SECONDARY_NAMENODE_HOST]
        else:
            snn_host_id = host_id_dic.values()[len(host_id_dic.values()) - 1]

        hdfs_service.create_role("{0}-snn".format(HDFS_NAMENODE_SERVICE_NAME), "SECONDARYNAMENODE", snn_host_id)

        dn_role_group = hdfs_service.get_role_config_group("{0}-DATANODE-BASE".format(SERVICE_NAME))
        dn_role_group.update_config(HDFS_DATANODE_CONFIG)

        gw_role_group = hdfs_service.get_role_config_group("{0}-GATEWAY-BASE".format(SERVICE_NAME))
        gw_role_group.update_config(HDFS_GATEWAY_CONFIG)

        datanode = 0
        for host in HDFS_DATANODE_HOSTS.split(","):
            datanode += 1
            dn_id = host_id_dic[host]
            hdfs_service.create_role("{0}-dn-".format(HDFS_NAMENODE_SERVICE_NAME) + str(datanode), "DATANODE", dn_id)

        gateway = 0
        for host in HDFS_GATEWAY_HOSTS.split(","):
            gateway += 1
            gateway_id = host_id_dic[host]
            hdfs_service.create_role("{0}-gw-".format(HDFS_NAMENODE_SERVICE_NAME) + str(gateway), "GATEWAY", gateway_id)

        # init_hdfs(hdfs_service, 180)
        if ENABLE_NN_HA == "true":
            enable_nn_ha(hdfs_service, host_id_dic)

        cluster.deploy_client_config()
    else:
        hdfs_service = cluster.get_service(SERVICE_NAME)

    return hdfs_service


# Initializes HDFS - format the file system
def init_hdfs(hdfs_service, timeout):
    cmd = hdfs_service.format_hdfs("{0}-nn".format(SERVICE_NAME))[0]
    if not cmd.wait(timeout).success:
        print "WARNING: Failed to format HDFS, attempting to continue with the setup"


def enable_nn_ha(hdfs_service, host_id_dic):
    if HDFS_SECONDARY_NAMENODE_HOST == "":
        snn_host_id = host_id_dic.values()[1]
    else:
        snn_host_id = host_id_dic[HDFS_SECONDARY_NAMENODE_HOST]

    """jns: List of Journal Nodes to be created during the command.
                Each element of the list must be a dict containing the following keys:
                  - B{jnHostId}: ID of the host where the new JournalNode will be created.
                  - B{jnName}: Name of the JournalNode role (optional)
                  - B{jnEditsDir}: Edits dir of the JournalNode. Can be omitted if the config
                    is already set at RCG level."""
    jns = list()
    error_msg = "当前集群只有" + bytes(len(host_id_dic)) + "台机器,少于三台,构不成HA的条件"
    if JN_HOSTS == "":
        if len(host_id_dic) < 3:
            print error_msg
            sys.exit(1)
        elif len(host_id_dic) <= 10:
            jn1_dic = {
                'jnHostId': host_id_dic.values()[0],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn2_dic = {
                'jnHostId': host_id_dic.values()[1],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn3_dic = {
                'jnHostId': host_id_dic.values()[2],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jns.append(jn1_dic)
            jns.append(jn2_dic)
            jns.append(jn3_dic)
        else:
            jn1_dic = {
                'jnHostId': host_id_dic.values()[0],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn2_dic = {
                'jnHostId': host_id_dic.values()[1],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn3_dic = {
                'jnHostId': host_id_dic.values()[2],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn4_dic = {
                'jnHostId': host_id_dic.values()[3],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jn5_dic = {
                'jnHostId': host_id_dic.values()[4],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jns.append(jn1_dic)
            jns.append(jn2_dic)
            jns.append(jn3_dic)
            jns.append(jn4_dic)
            jns.append(jn5_dic)
    else:
        for host in JN_HOSTS.split(","):
            jn_dic = {
                'jnHostId': host_id_dic[host],
                'jnEditsDir': DFS_JOURNALNODE_EDITS_DIR
            }
            jns.append(jn_dic)

    jnn_role_group = hdfs_service.get_role_config_group("{0}-JOURNALNODE-BASE".format(SERVICE_NAME))
    jnn_role_group.update_config(HDFS_JOURNALNODE_CONFIG)

    hdfs_service.enable_nn_ha(ACTIVE_NAME, snn_host_id, HDFS_NAMESERVICE, jns).wait()
