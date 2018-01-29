# -*- coding: utf-8 -*-
import threadpool, multiprocessing, os
from jdd_docker_http import get_container_info_by_container_name
from jdd_docker_http import delete_container
from jdd_docker_http import pull_docker_image
from jdd_docker_http import create_container
from jdd_docker_http import start_container
from utils.jdd_py_utils import get_os_env_exit

docker_tag_version = (os.getenv('DOCKER_TAG_VERSION'))

BRANCH = (os.getenv('GIT_BRANCH'))

pipelineCounter = (os.getenv('GO_PIPELINE_COUNTER'))

DOCKER_IMAGE_NAME = (os.getenv('DOCKER_IMAGE_NAME'))

DOCKER_IMAGE_NAME = get_os_env_exit('DOCKER_IMAGE_NAME')

IMAGE_TAG = docker_tag_version + '-' + BRANCH + '-' + pipelineCounter

current_docker = DOCKER_IMAGE_NAME + ':' + IMAGE_TAG

docker_container_name = (os.getenv('DOCKER_CONTAINER_NAME'))

PARAMTER_PORT = None

PARAMTER_VOLUME = (os.getenv('PARAMTER_VOLUME_LIST'))


# get container info
# exsit clean it and build new one
# !exsit build newone
def dowork(server):
    ip = server.get('ip')
    port = '2376'
    print 'start to dowork'
    container = get_container_info_by_container_name(ip, port, docker_container_name)
    if (container is not None and container != '!exsit' and len(container) > 0):
        print '1'
        res = delete_container(ip, port, docker_container_name)
        if res == '-1':
            raise Exception('something wrong when deleting older container,please check it manually')
        res = pull_docker_image(ip, port, DOCKER_IMAGE_NAME, IMAGE_TAG)
        if res == '-1':
            raise Exception('something woring when pulling docker image:' + DOCKER_IMAGE_NAME)
        res = create_container(ip, port, docker_container_name, current_docker, PARAMTER_PORT, PARAMTER_VOLUME)
        if res == '-1':
            raise Exception('something woring when creating container:' + DOCKER_IMAGE_NAME)
        res = start_container(ip, port, docker_container_name)
        if res == '-1':
            raise Exception('something woring when starting container:' + DOCKER_IMAGE_NAME)
    elif (container is None):
        print '2'
        # res = delete_container(ip, port, docker_container_name)
        # if res == '-1':
        #     raise Exception('something wrong when deleting older container,please check it manually')

        res = pull_docker_image(ip, port, DOCKER_IMAGE_NAME, IMAGE_TAG)
        if res == '-1':
            raise Exception('something woring when pulling docker image:' + DOCKER_IMAGE_NAME)

        res = create_container(ip, port, docker_container_name, current_docker, PARAMTER_PORT, PARAMTER_VOLUME)
        if res == '-1':
            raise Exception('something woring when creating container:' + DOCKER_IMAGE_NAME)

        res = start_container(ip, port, docker_container_name)
        if res == '-1':
            raise Exception('something woring when starting container:' + DOCKER_IMAGE_NAME)
    elif (container == '!exsit'):
        print '3'
        res = pull_docker_image(ip, port, DOCKER_IMAGE_NAME, IMAGE_TAG)
        if res == '-1':
            raise Exception('something woring when pulling docker image:' + DOCKER_IMAGE_NAME)
        res = create_container(ip, port, docker_container_name, current_docker, PARAMTER_PORT, PARAMTER_VOLUME)
        if res == '-1':
            raise Exception('something woring when creating container:' + DOCKER_IMAGE_NAME)
        res = start_container(ip, port, docker_container_name)
        if res == '-1':
            raise Exception('something woring when starting container:' + DOCKER_IMAGE_NAME)
    else:
        print '4'
        res = pull_docker_image(ip, port, DOCKER_IMAGE_NAME, IMAGE_TAG)
        if res == '-1':
            raise Exception('something woring when pulling docker image:' + DOCKER_IMAGE_NAME)
        res = create_container(ip, port, docker_container_name, current_docker, PARAMTER_PORT, PARAMTER_VOLUME)
        if res == '-1':
            raise Exception('something woring when creating container:' + DOCKER_IMAGE_NAME)
        res = start_container(ip, port, docker_container_name)
        if res == '-1':
            raise Exception('something woring when starting container:' + DOCKER_IMAGE_NAME)


server_num = int(os.getenv('SERVER_NUM'))
servers = []
if server_num > 0:
    for n in range(1, server_num + 1, 1):
        i = str(n)
        server_info = str(os.getenv('SERVER_' + i)).split(":")
        ip = str(server_info[1])
        port = str(server_info[2])
        user = str(server_info[0])
        passwd = str(os.getenv('SERVER_PASSWD_' + i))
        env_info_dict = {'ip': ip, 'port': port, 'user': user, 'passwd': passwd}
        servers.append(env_info_dict)

print servers
pool = threadpool.ThreadPool(multiprocessing.cpu_count())
requests = threadpool.makeRequests(dowork, servers)
for req in requests:
    pool.putRequest(req)
pool.wait()
