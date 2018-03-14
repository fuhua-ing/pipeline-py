# -*- coding: utf-8 -*-
from constants.jdd_common_constants import DOCKER_IMAGE_TAG, CURRENT_DOCKER_WITH_TAG
from constants.jdd_constants_from_env import DOCKER_CONTAINER_NAME, DOCKER_IMAGE_NAME, PARAMTER_PORT, \
    PARAMTER_ENTRYPOINT, PARAMTER_VOLUME, SERVER_INFO
from constants.jdd_docker_service import get_container_info_by_container_name, pull_docker_image, create_container, \
    start_container, delete_container

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
    start_container(ip, port, DOCKER_CONTAINER_NAME)
else:
    print 'start to delete the container'
    delete_container(ip, port, DOCKER_CONTAINER_NAME)
    pull_docker_image(ip, port, DOCKER_IMAGE_NAME, DOCKER_IMAGE_TAG)
    create_container(ip, port, DOCKER_CONTAINER_NAME, CURRENT_DOCKER_WITH_TAG, paramter_port=PARAMTER_PORT,
                     paramter_volume=PARAMTER_VOLUME, paramter_Entrypoint=PARAMTER_ENTRYPOINT)
    start_container(ip, port, DOCKER_CONTAINER_NAME)
