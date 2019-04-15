#!/bin/bash
source /etc/profile
PASSWD='s123456'
function expect_run_cmd {
  expect -c "set timeout -1;
        spawn $1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *assword:* {send -- $PASSWD\r;exp_continue;}
            *id_rsa):* {send -- \r;exp_continue}
            *y/n)?* {send -- y\r;exp_continue}
            *passphrase* {send -- \r;exp_continue}
            *Enter* {send -- $PASSWD\r;exp_continue;}
            *Password* {send -- $PASSWD\r;exp_continue;}
            eof        {exit 0;}
        }";
}
echo "begin set pgsql"
yum install --setopt=protected_multilib=false -y postgresql96-libs postgresql96-plperl postgresql96-plpython postgresql96-devel postgresql96 postgresql96-server
/usr/pgsql-9.6/bin/postgresql96-setup initdb
unalias cp
cp -f ./config/postgresql.conf /var/lib/pgsql/9.6/data
cp -f ./config/pg_hba.conf /var/lib/pgsql/9.6/data
alias cp='cp -i'
mkdir -p /var/log/postgresql
chown -R postgres:postgres /var/log/postgresql
chown -R postgres:postgres /var/lib/pgsql/9.6/data
cmd=`cat /etc/sysctl.conf|grep "kernel.sem"|wc -l`
if [[ "${cmd}" == "0" ]];then
  echo "kernel.sem=50100 128256000 50100 2560" >>/etc/sysctl.conf
else
  echo "kernel.sem exists"
fi
sysctl -p
systemctl restart postgresql-9.6
systemctl enable postgresql-9.6
expect_run_cmd "/usr/pgsql-9.6/bin/createuser -d -s -l -U postgres -h 127.0.0.1 -w -P root"
expect_run_cmd "psql -d postgres -U root -b -q -f ./config/create_oms_iad_db.sql"
#expect_run_cmd "psql -d oms_iad -U root -b -q -f ./config/oms_iad_jiegou.sql"
#expect_run_cmd "psql -d oms_iad -U root -b -q -f ./config/metric_metric.sql"
#expect_run_cmd "psql -d oms_iad -U root -b -q -f ./config/oms_iad_shuju.sql"
#expect_run_cmd "psql -d quartz -U root -b -q -f ./config/quartz.sql"
exit 0
