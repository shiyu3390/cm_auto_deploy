#!/bin/bash
source /etc/profile
systemctl restart redis
systemctl restart chronyd
timedatectl set-ntp yes
chronyc tracking
chown -R cloudera-scm:cloudera-scm /opt/cloudera/csd
chown cloudera-scm:cloudera-scm /opt/cloudera/parcels
rm -rf /var/lib/cloudera-scm-agent/*
#ps aux|grep supervisord|grep "cm"|awk '{print $2}'|xargs kill -9
systemctl restart cloudera-scm-agent
