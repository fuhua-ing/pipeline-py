# -*- coding: utf-8 -*-
from constants.jdd_constants_from_env import DOCKER_CONTAINER_NAME, DOCKER_IMAGE_NAME, PARAMTER_PORT, \
    PARAMTER_ENTRYPOINT, PARAMTER_VOLUME, SERVER_INFO, PIPELINE_ID, GO_PIPELINE_NAME, GIT_BRANCH, DOCKER_TAG_CLASSIFIER, \
    GO_JOB_NAME
from constants.jdd_docker_service import get_container_info_by_container_name, pull_docker_image, create_container, \
    start_container, delete_container
from constants.jdd_common_constants import spliter, DOCKER_BUILD_PATH
from constants.jdd_service import getCounterCode

url = 'http://192.168.136.158:8080/deploy/getCounterCode'
GO_PIPELINE_COUNTER = getCounterCode(url, PIPELINE_ID)

# docker image build path
DOCKER_BUILD_WORK_PATH = DOCKER_BUILD_PATH + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME

DOCKER_IMAGE_TAG = DOCKER_TAG_CLASSIFIER + '-' + GIT_BRANCH + '-' + GO_PIPELINE_COUNTER

CURRENT_DOCKER_WITH_TAG = DOCKER_IMAGE_NAME + ':' + DOCKER_IMAGE_TAG

ip = SERVER_INFO
port = '2376'
print 'start to deploy docker image to the server'
container = get_container_info_by_container_name(ip, port, DOCKER_CONTAINER_NAME)
if container == 'connect_error':
    exception = 'please check the target env,Network connect error,ip: ' + ip
    raise exception
elif (container is None or container == '!exsit'):
    print 'container is not !exist'
    status_code = pull_docker_image(ip, port, DOCKER_IMAGE_NAME, DOCKER_IMAGE_TAG)
    if status_code == '-1':
        exception = 'pull images failed'
        raise exception

    create_container(ip, port, DOCKER_CONTAINER_NAME, CURRENT_DOCKER_WITH_TAG, paramter_port=PARAMTER_PORT,
                     paramter_volume=PARAMTER_VOLUME, paramter_Entrypoint=PARAMTER_ENTRYPOINT)
    start_container(ip, port, DOCKER_CONTAINER_NAME, PARAMTER_PORT)
else:
    print 'start to delete the container'
    delete_container(ip, port, DOCKER_CONTAINER_NAME)
    pull_docker_image(ip, port, DOCKER_IMAGE_NAME, DOCKER_IMAGE_TAG)
    create_container(ip, port, DOCKER_CONTAINER_NAME, CURRENT_DOCKER_WITH_TAG, paramter_port=PARAMTER_PORT,
                     paramter_volume=PARAMTER_VOLUME, paramter_Entrypoint=PARAMTER_ENTRYPOINT)
    start_container(ip, port, DOCKER_CONTAINER_NAME, PARAMTER_PORT)
