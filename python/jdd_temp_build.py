# -*- coding: utf-8 -*-
import threadpool, paramiko, multiprocessing, traceback, os
from time import sleep
from jdd_common import DOCKER_IMAGE_NAME, DOCKER_CONTAINER_NAME, PARAMTER_PORT, \
    PARAMTER_VOLUME, DOCKER_TAG_VERSION, GIT_BRANCH, GO_PIPELINE_COUNTER

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect("192.168.136.77", 22, "root", "123qwe!@#")
stdin,stdout,stderr=ssh.exec_command('cd /data/work/crawler-lottery && bin/crawler stop')
print stdout.read()
print stderr.read()
log_path = '/root/temp/crawler-log/'+ GO_PIPELINE_COUNTER
stdin,stdout,stderr = ssh.exec_command('mkdir -p ' + log_path + ' && cp /data/work/crawler-lottery/log/* '+ log_path)
print stdout.read()
print stderr.read()

stdin,stdout,stderr=ssh.exec_command('rm -rf /data/work/crawler-lottery/*')
sleep(5)
print stdout.read()
print stderr.read()
stdin,stdou,stdout=ssh.exec_command('cd /data/work/crawler-lottery &&  curl -SL "http://maven-repository.jdddata.com/nexus/service/local/artifact/maven/redirect?r=public&g=com.jdddata.crawler&a=crawler-project-lottery&v=1.0.0-SNAPSHOT&c=install-2&p=tar.gz" -o crawler-project-lottery-1.0.0-SNAPSHOT-install-2.tar.gz')
print stdout.read()
print stderr.read()

stdin,stdout,stderr=ssh.exec_command('cd /data/work/crawler-lottery &&  tar -zxvf  crawler-project-lottery-1.0.0-SNAPSHOT-install-2.tar.gz && source /etc/profile && bin/crawler start')
print stdout.read()
print stderr.read()

sleep(8)

stdin,stdout,stderr=ssh.exec_command('curl http://192.168.136.77:31282/lottery-2/admin?cmd=start')
print stdout.read()
print stderr.read()
