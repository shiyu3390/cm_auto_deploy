#!/bin/bash
source /etc/profile
localIp=$1
allHosts=$2
sed -i "s/cmServer/${localIp}/g" ./config/clouderaconfig.ini
sed -i "s/allHosts/$allHosts/g" ./config/clouderaconfig.ini
function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    echo $(($num%$max+$min))
}

dataDirCount=`df -h|grep "bde_data"|wc -l`
if [[ "$dataDirCount" == "0" ]]; then
  sed -i "s/dataBaseDir//g" ./config/clouderaconfig.ini
  sed -i "s/dataDirs//g" ./config/clouderaconfig.ini
else
  dataDirList=`df -h|grep "bde_data"|awk '{print $6}'`
  rnd=$(rand 1 ${dataDirCount})
  sed -i "s/dataBaseDir/\/bde_data${rnd}/g" ./config/clouderaconfig.ini
  dataDirs=""
  i=0
  for dataDir in ${dataDirList}
  do
     let i+=1
     if [[ ${i} -eq 1 ]]; then
       dataDirs="$dataDir"
     else
       dataDirs="$dataDir,$dataDirs"
     fi
  done
  dataDirs=${dataDirs//\//\\/}
  sed -i "s/dataDirs/$dataDirs/g" ./config/clouderaconfig.ini
fi

#cd package/setuptools-40.2.0
#python setup.py install
#cd ../cm_api-19.1.1
#python setup.py install
cd ./script
pwd
python deploy_bde.py
