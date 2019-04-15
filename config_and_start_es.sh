#!/bin/bash
source /etc/profile
mkdir -p /var/log/elasticsearch
chown elasticsearch:elasticsearch /var/log/elasticsearch
chown -R elasticsearch:elasticsearch /etc/elasticsearch
dataDirCount=`df -h|grep "bde_data"|wc -l`
if [[ "$dataDirCount" == "0" ]]; then
  sed -i "s/dataPath/\/var\/lib\/elasticsearch/g" /etc/elasticsearch/elasticsearch.yml
else
  dataDirList=`df -h|grep "bde_data"|awk '{print $6}'`
  esDataPath=""
  i=0
  for dataDir in ${dataDirList}
  do
     let i+=1
     basePath=${dataDir}"/elasticsearch"
     mkdir -p ${basePath}
     chown elasticsearch:elasticsearch ${basePath}
     if [[ ${i} -eq 1 ]]; then
       esDataPath=${basePath}
     else
       esDataPath=${basePath}","${esDataPath}
     fi
  done
  esDataPath=${esDataPath//\//\\/}
  sed -i "s/dataPath/$esDataPath/g" /etc/elasticsearch/elasticsearch.yml
fi

cat /etc/hosts| while read line
do
  ip=`echo ${line}|awk '{print $1}'`
  hostName=`echo ${line}|awk '{print $2}'`
  if [[ "${hostName}" != "localhost" ]]; then
    c=`ip a|grep "$ip"|wc -l`
    if [[ "${c}" == "1" ]]; then
      isMaster=`cat /etc/elasticsearch/elasticsearch.yml|grep "$hostName"|wc -l`
      if [[ "${isMaster}" == "1" ]]; then
        sed -i "s/isMaster/true/g" /etc/elasticsearch/elasticsearch.yml
      else
        sed -i "s/isMaster/false/g" /etc/elasticsearch/elasticsearch.yml 
      fi
      sed -i "s/nodeName/$hostName/g" /etc/elasticsearch/elasticsearch.yml   
    fi
  fi
done

systemctl enable elasticsearch
chkconfig elasticsearch on
systemctl restart elasticsearch
