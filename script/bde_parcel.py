#!/usr/bin/env python
# coding=utf-8
import sys
import bde_config
import time

reload(sys)
sys.setdefaultencoding('utf-8')


# Downloads and distributes parcels
def deploy_parcels(cluster):
    parcels = cluster.get_all_parcels('full')
    for parcel in parcels:
        print "%s-%s status is %s" % (parcel.product, parcel.version, parcel.stage)
        if parcel.stage == "DOWNLOADED":
            print "%s-%s status is %s" % (parcel.product, parcel.version, parcel.stage)
            parcel.start_distribution()
            while True:
                p = cluster.get_parcel(parcel.product, parcel.version)
                if p.stage == "DISTRIBUTED":
                    break
                elif p.state.errors:
                    raise Exception(str(p.state.errors))
                print "%s-%s: %s / %s,status is %s" % (
                    p.product, p.version, p.state.progress, p.state.totalProgress, p.stage)
                time.sleep(15)
            print "%s-%s status is %s" % (
                parcel.product, parcel.version, cluster.get_parcel(parcel.product, parcel.version).stage)
            parcel.activate()
            while True:
                p = cluster.get_parcel(parcel.product, parcel.version)
                if p.stage == "ACTIVATED":
                    break
                elif p.state.errors:
                    raise Exception(str(p.state.errors))
                print "%s-%s: %s / %s,status is %s" % (
                    p.product, p.version, p.state.progress, p.state.totalProgress, p.stage)
                time.sleep(15)

            print "%s-%s status is %s" % (
                parcel.product, parcel.version, cluster.get_parcel(parcel.product, parcel.version).stage)
        elif parcel.stage == "DISTRIBUTED":
            print "%s-%s status is %s" % (
                parcel.product, parcel.version, cluster.get_parcel(parcel.product, parcel.version).stage)
            parcel.activate()
            while True:
                p = cluster.get_parcel(parcel.product, parcel.version)
                if p.stage == "ACTIVATED":
                    break
                elif p.state.errors:
                    raise Exception(str(p.state.errors))
                print "%s-%s: %s / %s,status is %s" % (
                    p.product, p.version, p.state.progress, p.state.totalProgress, p.stage)
                time.sleep(15)

            print "%s-%s status is %s" % (
                parcel.product, parcel.version, cluster.get_parcel(parcel.product, parcel.version).stage)
        elif parcel.stage == "ACTIVATED":
            print "%s-%s status is %s" % (
                parcel.product, parcel.version, cluster.get_parcel(parcel.product, parcel.version).stage)
