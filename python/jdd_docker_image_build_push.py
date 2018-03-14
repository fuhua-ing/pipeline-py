# -*- coding: utf-8 -*-

# 创建tar包工作目录
import os
from time import sleep
from constants.jdd_commands import C_docker_build, C_docker_push, C_docker_rm_local
from constants.jdd_common_constants import DOCKER_BUILD_WORK_PATH
from constants.jdd_constants_from_env import PROJECT_RESPOSITORY, GROUP_ID, ARTIFACT_ID, PROJECT_VERSION, \
    CLASSIFIER, PROJECT_PACKAGE_TYPE
from service.jdd_service import get_tar, get_tar_md5, get_dockerfile

os.system('rm -rf ' + DOCKER_BUILD_WORK_PATH)
os.system('mkdir -p ' + DOCKER_BUILD_WORK_PATH)

# 拉取远程nexus tar.gz
res = get_tar(PROJECT_RESPOSITORY, GROUP_ID, ARTIFACT_ID, PROJECT_VERSION, CLASSIFIER, PROJECT_PACKAGE_TYPE,
              DOCKER_BUILD_WORK_PATH)
sleep(5)
if res == '-1':
    raise Exception("download tar.gz failed,please check last step run successfully")

# 获取md5
md5 = get_tar_md5(DOCKER_BUILD_WORK_PATH)
if md5 != res:
    raise Exception("download tar.gz is not complete please try to run gocd again")

# 拉取docker file
get_dockerfile(DOCKER_BUILD_WORK_PATH)
sleep(3)

# docker build
# timestampLine = str(datetime.now().strftime('%Y%m%d%H%M%S'))
sleep(2)
os.system(
    'cd ' + DOCKER_BUILD_WORK_PATH + ' && ' + C_docker_build + ' && ' + C_docker_push + ' && ' + C_docker_rm_local)
