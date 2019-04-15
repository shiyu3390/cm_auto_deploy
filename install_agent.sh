#!/bin/bash
source /etc/profile
mkdir -p /home/sinorail
mkdir -p /var/log/monitor
mkdir -p /var/log/logStatistics
systemctl stop firewalld
systemctl disable firewalld
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0
sysctl -p
mkdir -p /etc/yum.repos.d/repo_bak
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/repo_bak/
mv /etc/yum.repos.d/repo_bak/bde.repo /etc/yum.repos.d/
yum clean all
yum install --setopt=protected_multilib=false keepalived nginx redis ntp lrzsz unzip rsync expect chrony jdk scala elasticsearch cloudera-manager-daemons cloudera-manager-agent -y
sed -i "s/bind 127.0.0.1/bind 0.0.0.0/g" /etc/redis.conf
systemctl enable redis
chkconfig redis on
systemctl enable chronyd
chkconfig chronyd on
mkdir -p /opt/cloudera/parcels
mkdir -p /opt/cloudera/csd
chown cloudera-scm:cloudera-scm /opt/cloudera/parcels
