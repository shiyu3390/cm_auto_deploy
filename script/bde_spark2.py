#!/usr/bin/env python
# coding=utf-8
import sys
import random
import bde_config
import bde_yarn

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
ALL_HOSTS = CONFIG.get("CDH", "cluster.hosts").strip()
SPARK2_HS_HOST = CONFIG.get("SPARK2", "spark.historyserver.host").strip()
SERVICE_NAME = "spark2_on_yarn"
SPARK2_SERVICE_CONFIG = {
    'yarn_service': bde_yarn.SERVICE_NAME
}

SPARK2_HS_CONFIG = {
    'max_log_backup_index': 1,
    'process_auto_restart': 'true',
    'oom_sigkill_enabled': 'false',
    'oom_heap_dump_dir': '/tmp',
    'history_server_retained_apps': 20,
    'role_config_suppression_log_dir': 'true',
    'role_config_suppression_oom_heap_dump_dir': 'true',
    'role_health_suppression_spark2_on_yarn_spark2_yarn_history_server_swap_memory_usage': 'true',
}

SPARK2_GATEWAY_CONFIG = {
    'spark_deploy_mode': 'cluster',
    'spark_kafka_version': '0.10',
    'spark_dynamic_allocation_enabled': 'false',
    'spark2-conf/spark-env.sh_client_config_safety_valve': '''export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_DIST_CLASSPATH=$SPARK_DIST_CLASSPATH:$(hbase classpath)''',
    'spark2-conf/spark-defaults.conf_client_config_safety_valve': '''spark.yarn.jars=hdfs://sinorail/spark/jars/*
spark.cores.max=16
spark.executor.cores=1
spark.executor.memory=1G
spark.default.parallelism=6
spark.driver.memory=1G
spark.speculation=true
spark.speculation.interval=100
spark.speculation.quantile=0.75
spark.speculation.multiplier=1.5
spark.ui.retainedJobs=50
spark.ui.retainedStage=50
spark.ui.retainedTasks=100
spark.sql.ui.retainedExecutions=50
spark.streaming.ui.retainedBatches=50
spark.ui.retainedDeadExecutors=50
spark.testing.reservedMemory=0'''
}


def deploy_spark2(cluster, host_id_dic, service_names):
    spark2_service = None
    if not service_names.__contains__(SERVICE_NAME):
        spark2_service = cluster.create_service(SERVICE_NAME, "SPARK2_ON_YARN")
        spark2_service.update_config(SPARK2_SERVICE_CONFIG)
        spark2_hs_id = host_id_dic.values()[random.randint(0, len(host_id_dic.values()) - 1)]
        if SPARK2_HS_HOST != "":
            spark2_hs_id = host_id_dic[SPARK2_HS_HOST]

        role = spark2_service.create_role("SPARK2_HISTORY_SERVER", "SPARK2_YARN_HISTORY_SERVER", spark2_hs_id)
        role.update_config(SPARK2_HS_CONFIG)

        gw = spark2_service.get_role_config_group("{0}-GATEWAY-BASE".format(SERVICE_NAME))
        gw.update_config(SPARK2_GATEWAY_CONFIG)

        gateway = 0
        for host in ALL_HOSTS.split(","):
            gateway += 1
            gateway_id = host_id_dic[host]
            spark2_service.create_role("{0}-gw-".format(SERVICE_NAME) + str(gateway), "GATEWAY", gateway_id)

        cluster.deploy_client_config()
    else:
        spark2_service = cluster.get_service(SERVICE_NAME)

    return spark2_service



