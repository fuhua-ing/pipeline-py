# -*- coding: utf-8 -*-
import os
from network.jdd_get_file import get_tar
from network.jdd_get_file import get_dockerfile
from jdd_common import workPath, spliter, GO_PIPELINE_NAME, GO_JOB_NAME, GO_PIPELINE_COUNTER, GIT_BRANCH, \
    PROJECT_PACKAGE_TYPE, PROJECT_VERSION, PROJECT_RESPOSITORY, GROUP_ID, ARTIFACT_ID, CLASSIFILER, DOCKER_IMAGE_NAME, \
    DOCKER_TAG_VERSION


def get_tar_md5():
    obj_file = curr_path + '/' + 'app-install.tar.gz'
    p = os.popen('md5sum ' + obj_file + " | awk '{print $1}'")
    str_line = list()
    for line in p.readlines():
        line = line.strip()
        if not len(line):
            continue
        str_line.append(line)
    pp = str_line[0]
    return pp


# 第一步创建临时工作目录
curr_path = workPath + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME

os.system('rm -rf ' + curr_path)
os.system('mkdir -p ' + curr_path)

# 拉取远程nexus tar.gz


res = get_tar(PROJECT_RESPOSITORY, GROUP_ID, ARTIFACT_ID, PROJECT_VERSION, CLASSIFILER, PROJECT_PACKAGE_TYPE, curr_path)
if res == '-1':
    raise Exception("download tar.gz failed,please check last step run successfully")
md5 = get_tar_md5()
if md5 != res:
    raise Exception("download tar.gz is not complete please try to run gocd again")

# 拉取docker file
get_dockerfile(curr_path)

# docker build

# timestampLine = str(datetime.now().strftime('%Y%m%d%H%M%S'))


current_docker = DOCKER_IMAGE_NAME + ':' + DOCKER_TAG_VERSION + '-' + GIT_BRANCH + '-' + GO_PIPELINE_COUNTER

C_docker_build = 'docker build -t ' + current_docker + ' .'
C_docker_push = 'docker push ' + current_docker
C_docker_rm_local = 'docker rmi ' + current_docker
os.system('cd ' + curr_path + ' && ' + C_docker_build + ' && ' + C_docker_push + ' && ' + C_docker_rm_local)
