#!/bin/bash
source /etc/profile
hostname=`hostname`
if [[ -n "$1" ]];then
   hostname="$1"
fi
sh create_es_index.sh ${hostname}

su hdfs -c "hdfs dfs -chmod +x /user"
hdfs dfs -mkdir -p /spark/jars
hdfs dfs -put ./package/sparkjars/*.jar /spark/jars
sh create_hbase_table.sh
ansible -i host_config_bak network -m copy -a "src=./package/log4j2.properties dest=/etc/hadoop/conf.cloudera.yarn/" -S
ansible -i host_config_bak network -m copy -a "src=./package/log4j2.properties dest=/etc/spark2/conf.cloudera.spark2_on_yarn/" -S