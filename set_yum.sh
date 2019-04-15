#!/bin/bash
echo "begin setup bde local yum repo"
host=$1
mkdir -p /etc/yum.repos.d/CentOS_repo_bak
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/CentOS_repo_bak/
cp ./config/cdh_local.repo /etc/yum.repos.d/
yum clean all
yum install --setopt=protected_multilib=false chrony httpd ansible createrepo ntp expect rsync -y
sed -i "s/#host_key_checking = False/host_key_checking = False/g" /etc/ansible/ansible.cfg
mkdir -p /var/www/html/centos
mkdir -p /var/www/html/centos/extra
mkdir -p /var/www/html/centos/update
mkdir -p /var/www/html/centos/x86_64
rm -rf /var/www/html/centos/x86_64/*
cp ./package/bde_yum/*.rpm /var/www/html/centos/x86_64/
createrepo -pdo /var/www/html/centos/update /var/www/html/centos/update
createrepo -pdo /var/www/html/centos/extra /var/www/html/centos/extra
createrepo -pdo /var/www/html/centos/x86_64 /var/www/html/centos/x86_64
echo "[bde]
name=bde repo
baseurl=http://${host}/centos/x86_64/
enabled=1
gpgcheck=0
" >/etc/yum.repos.d/bde.repo
service httpd restart
rm -rf /etc/yum.repos.d/cdh_local.repo
yum clean all
yum makecache
echo "set bde local yum is finished"