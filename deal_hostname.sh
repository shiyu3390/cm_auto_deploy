#!/bin/bash
source /etc/profile
cat /etc/hosts| while read line
do
  ip=`echo ${line}|awk '{print $1}'`
  hostName=`echo ${line}|awk '{print $2}'`
  if [[ "${hostName}" != "localhost" ]]; then
    c=`ip a|grep "$ip"|wc -l`
    if [[ "${c}" == "1" ]]; then
       localHostName=`hostname`
       if [[ "${localHostName}" == "localhost" || "${localHostName}" =~ "localhost" ]]; then
          hostnamectl set-hostname ${hostName}
          echo "${hostName}">/etc/hostname
       fi
    fi
  fi
done
