#!/bin/bash
source /etc/profile
cd /opt
tar xf setuptools-40.2.0.tar
cd setuptools-40.2.0
python setup.py install
cd ../
tar xf cm_api-19.1.1.tar
cd cm_api-19.1.1
python setup.py install
cd ../
rm -rf setuptools-40.2.0*
rm -rf cm_api-19.1.1*
