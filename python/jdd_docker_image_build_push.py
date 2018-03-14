# -*- coding: utf-8 -*-

# 创建tar包工作目录
import os
from time import sleep
from constants.jdd_common_constants import DOCKER_BUILD_PATH, spliter
from constants.jdd_constants_from_env import PROJECT_RESPOSITORY, GROUP_ID, ARTIFACT_ID, PROJECT_VERSION, \
    CLASSIFIER, PROJECT_PACKAGE_TYPE, GO_PIPELINE_NAME, GO_JOB_NAME, DOCKER_TAG_CLASSIFIER, \
    GIT_BRANCH, DOCKER_IMAGE_NAME, PIPELINE_ID
from constants.jdd_service import get_tar, get_tar_md5, get_dockerfile, getCounterCode

url = 'http://192.168.136.158:8080/make/getCounterCode'
GO_PIPELINE_COUNTER = getCounterCode(url, PIPELINE_ID)

# docker image build path
DOCKER_BUILD_WORK_PATH = DOCKER_BUILD_PATH + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME

DOCKER_IMAGE_TAG = DOCKER_TAG_CLASSIFIER + '-' + GIT_BRANCH + '-' + GO_PIPELINE_COUNTER

CURRENT_DOCKER_WITH_TAG = DOCKER_IMAGE_NAME + ':' + DOCKER_IMAGE_TAG

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
C_docker_build = 'docker build -t ' + CURRENT_DOCKER_WITH_TAG + ' .'
C_docker_push = 'docker push ' + CURRENT_DOCKER_WITH_TAG
C_docker_rm_local = 'docker rmi ' + CURRENT_DOCKER_WITH_TAG
# timestampLine = str(datetime.now().strftime('%Y%m%d%H%M%S'))
sleep(2)
os.system(
    'cd ' + DOCKER_BUILD_WORK_PATH + ' && ' + C_docker_build + ' && ' + C_docker_push + ' && ' + C_docker_rm_local)
