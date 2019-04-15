#!/bin/bash
echo "begin set cm_jdk_scala"
source /etc/profile
host=$1
unalias cp
yum install -y --setopt=protected_multilib=false lrzsz unzip zip jdk scala cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
mkdir -p /opt/cloudera/parcels
mkdir -p /opt/cloudera/csd
cp -f ./package/SPARK2_ON_YARN-2.2.0.cloudera2.jar /opt/cloudera/csd
cp -f ./package/*.parcel* /opt/cloudera/parcel-repo
cp -f ./config/manifest.json /opt/cloudera/parcel-repo
cp -f ./config/config.ini /etc/cloudera-scm-agent/
alias cp='cp -i'
sed -i "s/server_host=localhost/server_host=$host/g" /etc/cloudera-scm-agent/config.ini
chown cloudera-scm:cloudera-scm /opt/cloudera/parcels
chown -R cloudera-scm:cloudera-scm /opt/cloudera/csd
/usr/share/cmf/schema/scm_prepare_database.sh postgresql -h127.0.0.1 -uroot -ps123456 --scm-host localhost scm scm s123456
systemctl restart cloudera-scm-server
echo "set set cm_jdk_scala is finished"