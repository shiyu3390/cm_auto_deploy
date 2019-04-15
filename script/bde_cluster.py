#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config

reload(sys)
sys.setdefaultencoding('utf-8')

CONFIG = bde_config.get_config()
CLUSTER_NAME = CONFIG.get("CM", "cluster.name").strip()
CDH_VERSION = CONFIG.get("CDH", "version").strip()
FULL_VERSION = CONFIG.get("CDH", "fullVersion").strip()


def init_cluster(api):
    clusters = api.get_all_clusters()
    cluster = None
    for item in clusters.to_json_dict()[clusters.LIST_KEY]:
        if CLUSTER_NAME == item['displayName']:
            cluster = api.get_cluster(CLUSTER_NAME)
            break
    if cluster is None:
        cluster = api.create_cluster(CLUSTER_NAME, CDH_VERSION, FULL_VERSION)

    return cluster
