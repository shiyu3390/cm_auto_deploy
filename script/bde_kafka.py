#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config
import bde_zookeeper

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
KAFKA_HOSTS = CONFIG.get("KAFKA", "kafka.hosts").strip()
kafka_data_dirs = CONFIG.get("KAFKA", "kafka.log.dirs").strip()
KAFKA_LOG_DIRS = ""
if kafka_data_dirs != "":
    for data_dir in kafka_data_dirs.split(","):
        if data_dir.endswith("/"):
            data_dir = data_dir[0:len(data_dir) - 1]
        KAFKA_LOG_DIRS += data_dir + "/kafkaData,"
else:
    KAFKA_LOG_DIRS = "/var/local/kafka/data,"

kafka_replication_factor = CONFIG.get("KAFKA", "kafka.default.replication.factor").strip()
KAFKA_DEFAULT_REPLICATION_FACTOR = "2"
if kafka_replication_factor != "":
    KAFKA_DEFAULT_REPLICATION_FACTOR = kafka_replication_factor

kafka_num_partitions = CONFIG.get("KAFKA", "kafka.num.partitions").strip()
KAFKA_NUM_PARTITIONS = "6"
if kafka_num_partitions != "":
    KAFKA_NUM_PARTITIONS = kafka_num_partitions

kafka_broker_max_heap_size = CONFIG.get("KAFKA", "kafka.broker_max_heap_size").strip()
KAFKA_BROKER_MAX_HEAP_SIZE = "512"
if kafka_broker_max_heap_size != "":
    KAFKA_BROKER_MAX_HEAP_SIZE = kafka_broker_max_heap_size

SERVICE_NAME = "kafka"
KAFKA_SERVICE_CONFIG = {
    'num.partitions': KAFKA_NUM_PARTITIONS,
    'default.replication.factor': KAFKA_DEFAULT_REPLICATION_FACTOR,
    'offsets.topic.replication.factor': '2',
    'zookeeper.session.timeout.ms': '60000',
    'zookeeper_service': bde_zookeeper.SERVICE_NAME,
    'message.max.bytes': '5242880',
    'replica.fetch.max.bytes': '5242880',
    'num.replica.fetchers': '2',
    'unclean.leader.election.enable': 'true',
}
KAFKA_ROLE_CONFIG = {
    'oom_sigkill_enabled': 'false',
    'process_auto_restart': 'true',
    'log.dirs': KAFKA_LOG_DIRS[0:len(KAFKA_LOG_DIRS) - 1],
    'max_log_backup_index': '1',
    'broker_max_heap_size': KAFKA_BROKER_MAX_HEAP_SIZE,
    'oom_heap_dump_dir': '/tmp',
    'role_health_suppression_kafka_kafka_broker_swap_memory_usage': 'true',
    'role_config_suppression_log_dir': 'true',
    'role_config_suppression_oom_heap_dump_dir': 'true',
}


# Deploys and initializes Kafka
def deploy_kafka(cluster, host_id_dic, host_ip_dic, service_names):
    # if platform.system() == 'Linux':
    #     for log_dir in KAFKA_LOG_DIRS.split(","):
    #         if not os.path.exists(log_dir):
    #             os.makedirs(log_dir)
    #         os.system("chown -R kafka:kafka " + log_dir)

    kafka = None
    if not service_names.__contains__(SERVICE_NAME):
        kafka = cluster.create_service(SERVICE_NAME, "KAFKA")
        kafka.update_config(KAFKA_SERVICE_CONFIG)
        kafka_host_ids = list()

        host_id_list = host_id_dic.values()
        if KAFKA_HOSTS == "":
            for host_id in host_id_list:
                kafka_host_ids.append(host_id)
        else:
            for host in KAFKA_HOSTS.split(","):
                kafka_host_ids.append(host_id_dic[host])

        broker_id = 0
        # role_names = []
        for host_id in kafka_host_ids:
            broker_id += 1
            KAFKA_ROLE_CONFIG['broker.id'] = broker_id
            role_name = SERVICE_NAME + "-" + str(broker_id)
            role = kafka.create_role(role_name, "KAFKA_BROKER", host_id)
            role.update_config(KAFKA_ROLE_CONFIG)
            advertised = "advertised.listeners=PLAINTEXT://" + host_ip_dic[host_id] + ":9092"
            kafka_advertised_conf = {
                'kafka.properties_role_safety_valve': advertised
            }
            role.update_config(kafka_advertised_conf)
            # role_names.append(role_name)

        cluster.deploy_client_config()
    else:
        kafka = cluster.get_service(SERVICE_NAME)

    return kafka
