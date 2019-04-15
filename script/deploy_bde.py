#!/usr/bin/env python
# coding=utf-8
import sys
import time
import bde_api
import bde_cluster
import bde_hbase
import bde_hdfs
import bde_host
import bde_kafka
import bde_parcel
import bde_service
import bde_spark2
import bde_yarn
import bde_zookeeper

reload(sys)
sys.setdefaultencoding('utf-8')


def start_service(service, cluster, service_name):
    begin_start = True
    if not "STARTED" == service.serviceState:
        while True:
            time.sleep(30)
            service = cluster.get_service(service_name)
            if "STOPPED" == service.serviceState and begin_start:
                service.start()
                begin_start = False
            print service_name, "serviceState: ", service.serviceState
            # "GOOD_HEALTH" == service.entityStatus
            if "STARTED" == service.serviceState or "STARTING" == service.serviceState:
                break


def wait_service_start(service, service_name):
    if not "STARTED" == service.serviceState:
        service.start().wait()
        print service_name, "deploy successfully"
    else:
        print service_name, "已经启动"


if __name__ == '__main__':
    begin_time = time.time()

    api = bde_api.get_api()
    # 初始化一个集群
    cluster = bde_cluster.init_cluster(api)
    if cluster is not None:
        print "Initialized cluster " + cluster.displayName + " which uses CDH version " + cluster.fullVersion
    else:
        print "初始化集群失败"
        sys.exit(1)

    # 添加机器到集群中
    cluster, host_id_dic, host_ip_dic = bde_host.add_hosts(cluster, api)
    print "hosts info:", host_id_dic
    # 添加cloudera manager监控服务
    bde_service.deploy_management(bde_api.get_cloudera_manager(api), host_id_dic)

    # 分发parcel文件并激活
    bde_parcel.deploy_parcels(cluster)

    # 获取集群上已有的服务列表
    service_list = cluster.get_all_services(view='FULL')
    service_names = list()
    for service in service_list:
        service_names.append(service.name)

    # 添加Zookeeper服务
    zookeeper = bde_zookeeper.deploy_zookeeper(cluster, host_id_dic, service_names)
    start_service(zookeeper, cluster, bde_zookeeper.SERVICE_NAME)
    print bde_zookeeper.SERVICE_NAME, "deploy successfully"

    # 添加Kafka服务
    kafka = bde_kafka.deploy_kafka(cluster, host_id_dic, host_ip_dic, service_names)
    start_service(kafka, cluster, bde_kafka.SERVICE_NAME)
    print bde_kafka.SERVICE_NAME, "deploy successfully"

    # 添加HDFS服务
    hdfs = bde_hdfs.deploy_hdfs(cluster, host_id_dic, service_names)

    # 休眠5分钟等待HDFS初始化和启用HA完成
    if not "STARTED" == hdfs.serviceState:
        time.sleep(300)
        hdfs.restart()
        while True:
            time.sleep(10)
            hdfs = cluster.get_service(bde_hdfs.SERVICE_NAME)
            if "STARTED" == hdfs.serviceState:
                break
    print bde_hdfs.SERVICE_NAME, "deploy successfully"
    # wait_service_start(hdfs, bde_hdfs.SERVICE_NAME)

    # 添加Hbase服务
    hbase = bde_hbase.deploy_hbase(cluster, host_id_dic, service_names)
    start_service(hbase, cluster, bde_hbase.SERVICE_NAME)
    print bde_hbase.SERVICE_NAME, "deploy successfully"

    # 添加YARN服务
    yarn = bde_yarn.deploy_yarn(cluster, host_id_dic, service_names)
    start_service(yarn, cluster, bde_yarn.SERVICE_NAME)
    print bde_yarn.SERVICE_NAME, "deploy successfully"

    # 添加Spark2服务
    spark2 = bde_spark2.deploy_spark2(cluster, host_id_dic, service_names)
    spark2.create_spark_job_history_dir().wait()
    start_service(spark2, cluster, bde_spark2.SERVICE_NAME)
    print bde_spark2.SERVICE_NAME, "deploy successfully"

    # 部署客户端配置
    cluster.restart(redeploy_client_configuration=True)
    while True:
        time.sleep(10)
        hdfs = cluster.get_service(bde_hdfs.SERVICE_NAME)
        if "STARTED" == hdfs.serviceState:
            break

    end_time = time.time()
    print "deploy finished,use " + str(end_time - begin_time) + "s"
