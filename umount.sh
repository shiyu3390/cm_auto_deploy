source /etc/profile
systemctl stop elasticsearch
systemctl stop cloudera-scm-agent
dataDir=`df -h|grep "bde_data"|awk '{print $6}'`
for data in ${dataDir}
do
  umount $data
  rm -rf $data
done
rm -rf /bde_data1
