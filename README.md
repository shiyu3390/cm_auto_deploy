# cm_auto_deploy

前提条件：做好本地yum源，yum源包含httpd ansible createrepo keepalived nginx redis ntp lrzsz unzip rsync expect chrony jdk scala elasticsearch cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server，放在package/bde_yum目录下，自行下载CDH、KAFKA、SPARK2的parcel文件，以及相应的sha文件，还有SPARK2_ON_YARN-2.2.0.cloudera2.jar

1. 编辑host_config文件
2. 如果机器都有主机名且不是localhost，编辑hostsOld文件，配置host映射
3. 如果需要定制每个节点部署哪些服务以及个服务的配置，编辑config/clouderaconfig.ini文件
4. 如果需要部署elasticsearch且需要定制elasticsearch的jvm配置和数据目录等，编辑config/elasticsearch.yml文件和config/jvm.options文件；不过不需要就将begin_deploy.sh脚本中与elasticsearch相关的注释掉
5. 最后执行sh begin_deploy.sh localIp ntpServerIp即可(localIp是当前脚本所在机器的IP，ntpServerIp是能够提供ntp服务的机器IP，如果没有则使用localIp代替)