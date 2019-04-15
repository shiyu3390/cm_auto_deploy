#!/bin/bash
localIp=$1
systemctl stop firewalld
systemctl disable firewalld
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0
sh set_yum.sh ${localIp}
if [[ $? -ne 0 ]]; then
  echo "设置本地yum源出错,请检查是否有相关的包冲突"
  exit 1
fi

ntpServer="$localIp"
if [[ -n "$2" ]];then
   ntpServer=$2
fi

allHosts="$localIp"
echo "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4" >hosts
echo "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6" >>hosts

s3=`echo "${localIp}"|awk -F '.' '{print $3}'`
s4=`echo "${localIp}"|awk -F '.' '{print $4}'`
localHostName="bde$s3-$s4"

ipList=`cat host_config|awk '{print $1}'`
hostCount=0
esMasterHosts=""
esMasterCount=0
for ip in ${ipList}
do
    let hostCount+=1
    s3=`echo "${ip}"|awk -F '.' '{print $3}'`
    s4=`echo "${ip}"|awk -F '.' '{print $4}'`
    hostname="bde$s3-$s4"
    if [[ -f "hostsOld" ]]; then
      line=`cat hostsOld|grep "${ip}"`
      hostNameOld=`echo "${line}"|awk '{print $2}'`
      if [[ "${hostNameOld}" == "" || "${line}" == "" ]]; then
        echo "hostsOld文件中没有给${ip}配置主机名映射,将使用${ip} ${hostname}作为hosts映射"
        echo "$ip $hostname" >>hosts
      else
        echo "$ip $hostNameOld" >>hosts
      fi
    else
      echo "没有配置hostsOld文件,将使用${ip} ${hostname}作为hosts映射"
      echo "$ip $hostname" >>hosts
    fi

    if [[ "${ip}" != "${localIp}" ]]; then
        allHosts="$allHosts,$ip"
    fi

    if [[ ${hostCount} -lt 4 ]]; then
        let esMasterCount+=1
	    line=`cat hosts|grep "${ip}"`
        esHostName=`echo "${line}"|awk '{print $2}'`
        if [[ ${hostCount} -eq 1 ]]; then
           esMasterHosts="\"$esHostName\""
        else
           esMasterHosts="\"$esHostName\",$esMasterHosts"
        fi
    fi
done

minimumMasterNodes=$(($esMasterCount/2+1))
sed -i "s/esMasterHosts/$esMasterHosts/g" ./config/elasticsearch.yml
sed -i "s/minimumMasterNodes/$minimumMasterNodes/g" ./config/elasticsearch.yml

echo "allHosts: $allHosts"
cat host_config >host_config_bak
sed -i '1i\[network]' host_config_bak
unalias cp
cp -f ./config/sysctl.conf /etc/
cp -f ./config/limits.conf /etc/security/
cp -f hosts /etc/
alias cp='cp -i'

sed -i 's/server 0.centos.pool.ntp.org iburst/#server 0.centos.pool.ntp.org iburst/g' /etc/chrony.conf
sed -i 's/server 1.centos.pool.ntp.org iburst/#server 1.centos.pool.ntp.org iburst/g' /etc/chrony.conf
sed -i 's/server 2.centos.pool.ntp.org iburst/#server 2.centos.pool.ntp.org iburst/g' /etc/chrony.conf
sed -i "s/server 3.centos.pool.ntp.org iburst/server $ntpServer iburst/g" /etc/chrony.conf
if [[ "${ntpServer}" == "${localIp}" ]]; then
   sed -i "s/#allow 192.168.0.0\/16/allow 192.168.0.0\/16/g" /etc/chrony.conf
   sed -i "s/#local stratum 10/local stratum 10/g" /etc/chrony.conf
fi
systemctl restart chronyd
systemctl enable chronyd
timedatectl set-ntp yes
chronyc tracking
sh ./set_pgsql.sh
if [[ $? -ne 0 ]]; then
  echo "部署pgsql出错,请检查"
  exit 1
fi

sh ./cm_pre.sh ${localIp}
if [[ $? -ne 0 ]]; then
  echo "部署和初始化cloudera-scm-server出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m copy -a "src=hosts dest=/etc/" -S
ansible -i host_config_bak network -m copy -a "src=./config/sysctl.conf dest=/etc/" -S
ansible -i host_config_bak network -m copy -a "src=./config/limits.conf dest=/etc/security/" -S
ansible -i host_config_bak network -m copy -a "src=/etc/yum.repos.d/bde.repo dest=/etc/yum.repos.d/" -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行拷贝文件出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m script -a ./deal_hostname.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行deal_hostname.sh脚本出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m script -a ./install_agent.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行install_agent.sh脚本出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m copy -a "src=/etc/chrony.conf dest=/etc/" -S
ansible -i host_config_bak network -m copy -a "src=/etc/cloudera-scm-agent/config.ini dest=/etc/cloudera-scm-agent/" -S
ansible -i host_config_bak network -m copy -a "src=./package/SPARK2_ON_YARN-2.2.0.cloudera2.jar dest=/opt/cloudera/csd/" -S
ansible -i host_config_bak network -m copy -a "src=./package/setuptools-40.2.0.tar dest=/opt/" -S
ansible -i host_config_bak network -m copy -a "src=./package/cm_api-19.1.1.tar dest=/opt/" -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行拷贝文件出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m script -a ./install_cmapi.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行install_cmapi.sh脚本出错,请检查"
  exit 1
fi

echo "开始执行挂盘操作"
source /etc/profile
ansible -i host_config_bak network -m script -a ./mount_disk.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行mount_disk.sh脚本出错,请检查"
  exit 1
fi

#部署配置ES,如果不需要全文检索请将下面注释掉
ansible -i host_config_bak network -m copy -a "src=./config/elasticsearch.yml dest=/etc/elasticsearch/" -S
ansible -i host_config_bak network -m copy -a "src=./config/jvm.options dest=/etc/elasticsearch/" -S
ansible -i host_config_bak network -m copy -a "src=./config/log4j2.properties dest=/etc/elasticsearch/" -S
ansible -i host_config_bak network -m script -a ./config_and_start_es.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行config_and_start_es.sh脚本出错,请检查"
  exit 1
fi
echo "elasticsearch安装配置完成,后续请通过手动执行sh create_es_index.sh ${localIp}创建索引"

ansible -i host_config_bak network -m script -a ./start_agent.sh -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行start_agent.sh脚本出错,请检查"
  exit 1
fi

sleep 60
echo "启动server和agent成功,开始自动化部署zookeeper、hdfs、kafka等BDE服务"
sh install_config_bigdata_service.sh ${localIp} ${allHosts}
if [[ $? -ne 0 ]]; then
  echo "自动化部署zookeeper、hdfs、kafka等BDE服务出错,请检查"
  exit 1
fi

ansible -i host_config_bak network -m copy -a "src=./package/log4j2.properties dest=/etc/hadoop/conf.cloudera.yarn/" -S
ansible -i host_config_bak network -m copy -a "src=./package/log4j2.properties dest=/etc/spark2/conf.cloudera.spark2_on_yarn/" -S
ansible -i host_config_bak network -m script -a ./replay_spark_related_jars.sh -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/elasticsearch-hadoop-6.0.0.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/kafka_2.11-1.0.1-kafka-3.1.0-SNAPSHOT.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/kafka-clients-1.0.1-kafka-3.1.0-SNAPSHOT.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/kafka-streams-1.0.1-kafka-3.1.0-SNAPSHOT.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/kafka-tools-1.0.1-kafka-3.1.0-SNAPSHOT.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/metrics-core-2.2.0.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/kafka-1.0.1/zkclient-0.10.jar dest=/opt/cloudera/parcels/SPARK2-2.2.0.cloudera2-1.cdh5.12.0.p0.232957/lib/spark2/kafka-0.10/" -S
ansible -i host_config_bak network -m copy -a "src=./package/hadoop-mapreduce-client-core-2.6.0-cdh5.11.1.jar dest=/opt/cloudera/parcels/CDH/jars/" -S
if [[ $? -ne 0 ]]; then
  echo "ansible执行拷贝文件出错,请检查"
  exit 1
fi
sleep 60

echo "部署完成,请用浏览器访问："${localIp}":7180 用户名admin,密码admin"
echo "请用浏览器确认BDE服务zookeeper、hdfs、hbase运行是否正常,如果正常,请手动执行脚本创建ES索引和hbase表:
      sh create_es_and_hbase_table.sh ${localIp}"
