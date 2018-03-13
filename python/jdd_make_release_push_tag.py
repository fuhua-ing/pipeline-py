# -*- coding: utf-8 -*-
import os, re
from time import sleep
from jdd_common import GO_PIPELINE_COUNTER, GO_JOB_NAME, GO_PIPELINE_NAME, spliter, workPath, GIT_URL, GIT_BRANCH



os.system('rm -rf ' + code_release)
os.system('mkdir -p ' + code_release)

code_release_path = code_release + spliter + code_last_dir




os.system(
    'cd ' + code_path + ' && git commit -am "release" && ' + 'git tag -a ' + GIT_BRANCH + '-release ' + ' -m "release"')

status_git_push = os.system('cd ' + code_path + ' && ' + ' git push origin ' + GIT_BRANCH + '-release')
sleep(2)
if status_git_push != 0:
    raise Exception('failed to push tag to remote repository')
print 'success push tag to remote'

status_deploy = os.system(
    'cd ' + code_release + ' && ' + 'git clone -b ' + GIT_BRANCH + '-release ' + GIT_URL + ' && cd ' + code_release_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean deploy -U')
if status_deploy != 0:
    raise Exception('deploy tar.gz from tag branch code error please check')
