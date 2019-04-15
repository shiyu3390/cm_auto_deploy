# cm_auto_deploy

1. 编辑host_config文件
2. 如果机器都有主机名且不是localhost，编辑hostsOld文件，配置host映射
3. 如果需要定制每个节点部署哪些服务以及个服务的配置，编辑config/clouderaconfig.ini文件
4. 如果需要部署elasticsearch且