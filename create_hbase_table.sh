#!/bin/bash
echo "create 'monitor120ExtendHistory',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}"| hbase shell
echo "create 'monitor120History',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor15ExtendHistory',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor15ExtendLive',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor1ExtendHistory',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor1ExtendLive',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor30ExtendHistory',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor30History',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor5ExtendHistory',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor5History',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitorDay',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitorDayExtend',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'homedata',{NAME=>'cf1', COMPRESSION => 'SNAPPY'}" | hbase shell

echo "create 'monitor5Live',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor30Live',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor120Live',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell

echo "create 'monitor5ExtendLive',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor30ExtendLive',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell
echo "create 'monitor120ExtendLive',{NAME => 'cf1', TTL => '172800', COMPRESSION => 'SNAPPY'}" | hbase shell
