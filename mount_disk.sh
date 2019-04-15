#!/bin/bash
function expect_run_cmd {
  expect -c "set timeout -1;
        spawn $1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *assword:* {send -- $PASSWD\r;exp_continue;}
            *id_rsa):* {send -- \r;exp_continue}
            *y/n)?* {send -- y\r;exp_continue}
            *y,n)?* {send -- y\r;exp_continue}
            *passphrase* {send -- \r;exp_continue}
            *Enter* {send -- $PASSWD\r;exp_continue;}
            *Password* {send -- $PASSWD\r;exp_continue;}
            eof        {exit 0;}
        }";
}
source /etc/profile
diskList=`fdisk -l | grep -o "^Disk /dev/[shv]d[a-z]"|awk '{print $2}'|sort`
dataCount=`df -h|grep "bde_data"|awk '{print $6}'|wc -l`
i=${dataCount}
sed -i "/bde_data/d" /etc/fstab
for disk in ${diskList}
do
  name=`echo ${disk}|awk -F "/dev/" '{print $2}'`
  count=`lsblk|grep "$name" |wc -l`
  dfCount=`df -h|grep "$disk"|wc -l`
  echo "$disk" "$count" "$dfCount"
  if [[ "$count" == "1" && "$dfCount" == "0" && ${i} -lt 11 ]];then
    let i+=1
    dataDir="/bde_data${i}"
    expect_run_cmd "mkfs.xfs -f ${disk}"
    mkdir -p ${dataDir}
    mount ${disk} ${dataDir}
    echo "${disk} ${dataDir} xfs defaults 0 0" >>/etc/fstab
  fi
done
