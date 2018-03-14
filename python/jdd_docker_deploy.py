# -*- coding: utf-8 -*-
import threadpool, multiprocessing, os
from python.constants.jdd_common_constants import DOCKER_IMAGE_TAG, CURRENT_DOCKER_WITH_TAG
from python.constants.jdd_constants_from_env import DOCKER_CONTAINER_NAME, DOCKER_IMAGE_NAME, PARAMTER_PORT, \
    PARAMTER_ENTRYPOINT, PARAMTER_VOLUME
from python.service.jdd_docker_service import get_container_info_by_container_name, pull_docker_image, create_container, \
    start_container, delete_container

exception = ''


# get container info
# exsit clean it and build new one
# !exsit build newone
def dowork(server):
    ip = server.get('ip')
    port = '2376'
    print 'start to dowork'
    container = get_container_info_by_container_name(ip, port, DOCKER_CONTAINER_NAME)
    if container == 'connect_error':
        global exception
        exception = 'please check the target env,Network connect error,ip: ' + ip
        return
    elif (container is None or container == '!exsit'):
        print 'container is not !exist'
        pull_docker_image(ip, port, DOCKER_IMAGE_NAME, DOCKER_IMAGE_TAG)
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


server_num = int(os.getenv('SERVER_NUM'))
servers = []
if server_num > 0:
    for n in range(1, server_num + 1, 1):
        i = str(n)
        server_info = str(os.getenv('SERVER_' + i)).split(":")
        ip = str(server_info[1])
        port = str(server_info[2])
        user = str(server_info[0])
        passwd = os.getenv('SERVER_PASSWD_' + i)
        env_info_dict = {'ip': ip, 'port': port, 'user': user, 'passwd': passwd}
        servers.append(env_info_dict)

print servers
pool = threadpool.ThreadPool(multiprocessing.cpu_count())
requests = threadpool.makeRequests(dowork, servers)
for req in requests:
    pool.putRequest(req)
pool.wait()

if exception is not None and len(exception) > 0:
    raise exception
