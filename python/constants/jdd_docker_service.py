# -*- coding: utf-8 -*-
import httplib, socket, ssl, traceback, json
from _ssl import PROTOCOL_TLSv1_2

from jdd_common_constants import Http_Success_code

ca_cert_file = '/data/gocd/python/pipeline-py/python/cert/ca.pem'
key_file = '/data/gocd/python/pipeline-py/python/cert/key.pem'
cert_file = '/data/gocd/python/pipeline-py/python/cert/cert.pem'

container_info_all = '/containers/json?all=true'
container_stop = '/containers/{0}/stop'
container_delete = '/containers/{0}'
container_create = '/containers/create?name={0}'

image_pull = '/images/create?fromImage={0}&tag={1}'

socket.setdefaulttimeout(1200000)


def del_last_char(str):
    str_list = list(str)
    str_list.pop()
    return "".join(str_list)


def docker_generateBody(current_docker, paramter_ports, paramter_volume,
                        paramter_Entrypoint):
    '''{"Env": ["FOO=bar","BAZ=quux"],"Cmd": ["date"],"Entrypoint": "","Image": "ubuntu","HostConfig": {"Binds": ["/tmp:/tmp"],"PortBindings": {"22/tcp": [{"HostPort": "11022"}]}}}'''
    image = '"Image":' + '"' + current_docker + '"'
    ports = ''
    volumes = ''
    entrypoint = ''
    HostConfig = ''

    if paramter_ports is not None:
        port_line = ''
        for port in paramter_ports.split(','):
            print port
            port_line = port_line + '"' + port.split(':')[1] + '/tcp"' + ':' + '[{"HostIP": "0.0.0.0", "HostPort":' + '"' + port.split(':')[0] + '"' + '}],'
        print port_line
        port_content = del_last_char(port_line)
        ports = '"PortBindings":{' + port_content + '}'
        print 'the binding ports is: ' + ports

    if paramter_volume is not None:
        volumeLine = ''
        for v in paramter_volume.split(','):
            volumeLine = volumeLine + '"' + v + '"' + ','
        volume_content = del_last_char(volumeLine)
        volumes = volumes + '"Binds":[' + volume_content + ']'

    if paramter_Entrypoint is not None:
        entrypointList = paramter_Entrypoint.split(",")
        entrypointLine = ''
        for entry in entrypointList:
            entrypointLine = entrypointLine + '"' + entry + '",'
        entrypoint_content = del_last_char(entrypointLine)
        entrypoint = '"Entrypoint":[' + entrypoint_content + ']'

    print volumes

    if (ports is not None and ports.strip() != "") and (volumes is not None and volumes.strip() != ""):
        print 'hostconfig 1'
        HostConfig = '"HostConfig":{' + ports + ',' + volumes + '}'

    if (ports is not None and ports.strip() != "") and (volumes is None or volumes.strip() == ""):
        print 'hostconfig 2'
        HostConfig = '"HostConfig":{' + ports + '}'

    if (ports is None or ports.strip() == "") and (volumes is not None and volumes.strip() != ""):
        print 'hostconfig 3'
        HostConfig = '"HostConfig":{' + volumes + '}'

    body = '{' + image
    if entrypoint is not None and len(entrypoint) > 0:
        body = body + ',' + entrypoint
    if HostConfig is not None and len(HostConfig) > 0:
        body = body + ',' + HostConfig
    print HostConfig
    body = body + '}'
    return body


def get_container_info_by_container_name(host, port, name):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        httpsConn.request('GET', container_info_all)
        res = httpsConn.getresponse()
        http_code = res.status
        http_resp = res.read()
        print('get_container_info_by_container_name status: %d' % http_code)
        print('get_container_info_by_container_name reponse %s' % http_resp)
        if http_code not in Http_Success_code:
            print 'get container info time out!!'
            return 'time_out'
        else:
            print 'success get the container info'
            res_json = json.loads(http_resp)
            container_names = []
            for container in res_json:
                container_name_list = container['Names']
                print container_name_list
                container_name = container_name_list[0]
                container_names.append(container_name.encode("utf-8"))
            cc = '/' + name
            if cc in container_names:
                print 'container exist'
                return cc
            else:
                print 'The specifect container is not exist'
                return "!exsit"
    except Exception, e:
        print e
        print 'python is in exception!'
        return 'connect_error'
    finally:
        if httpsConn:
            httpsConn.close()


def delete_container(host, port, name):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        stop_path = container_stop.replace("{0}", name)
        print stop_path
        httpsConn.request('POST', stop_path)
        res = httpsConn.getresponse()
        http_code = res.status
        http_resp = res.read()
        print('stop_container status: %d' % http_code)
        print('stop_container reponse %s' % http_resp)
        if http_code in Http_Success_code:
            delete_path = container_delete.replace("{0}", name)
            httpsConn.request('DELETE', delete_path)
            res = httpsConn.getresponse()
            http_code = res.status
            http_resp = res.read()
            print('delete_container status: %d' % http_code)
            print('delete_container reponse %s' % http_resp)
            if http_code not in Http_Success_code:
                return '-1'
    except Exception:
        print traceback.format_exc()
        return 'connect_error'
    finally:
        if httpsConn:
            httpsConn.close()


def create_container(host, port, docker_container_name, current_docker, paramter_port, paramter_volume,
                     paramter_Entrypoint):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        # body = '{"Image":"$IMAGE","PortBindings": { "$CONTAINER_PORT/tcp": [{ "HostPort": "$HOST_PORT" }]}}'
        # body = '{"Image":"docker-registry.jdddata.com/jdddata/dac-schedule:snapshot-1.0.0-81" , "HostConfig":{"Binds":["/root/gezhiwei/log:/usr/local/app/log"]}}'

        body = docker_generateBody(current_docker, paramter_port, paramter_volume, paramter_Entrypoint)

        print body
        path = container_create.replace("{0}", docker_container_name)
        httpsConn.request(method='POST', url=path, body=body,
                          headers={"Content-Type": "application/json"})
        res = httpsConn.getresponse()
        http_code = res.status
        http_resp = res.read()
        print('create_container status: %d' % http_code)
        print('create_container reponse %s' % http_resp)
        if http_code not in Http_Success_code:
            return '-1'
    except Exception:
        print traceback.format_exc()
        return 'connect_error'
    finally:
        if httpsConn:
            httpsConn.close()


def start_container(host, port, container_name):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        httpsConn.request(method='POST', url='/containers/' + container_name + '/start',
                          headers={"Content-Type": "application/json"})
        res = httpsConn.getresponse()
        http_code = res.status
        http_resp = res.read()
        print('start_container status: %d' % http_code)
        print('start_container reponse %s' % http_resp)
        if http_code not in Http_Success_code:
            return '-1'
    except Exception:
        print traceback.format_exc()
        return 'connect_error'
    finally:
        if httpsConn:
            httpsConn.close()


def pull_docker_image(host, port, name, tag):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        path = image_pull.replace("{0}", name).replace("{1}", tag)
        print path
        httpsConn.request(method='POST', url=path, headers={"Content-Type": "application/json"}, body=None)
        res = httpsConn.getresponse()
        http_code = res.status
        http_resp = res.read()
        print('status: %d' % http_code)
        print('reponse %s' % http_resp)
        if http_code not in Http_Success_code:
            return '-1'
        else:
            return '0'
    except Exception:
        print traceback.format_exc()
        return 'connect_error'
    finally:
        if httpsConn:
            httpsConn.close()

# body = '{"Image":"$IMAGE","PortBindings": { "$CONTAINER_PORT/tcp": [{ "HostPort": "$HOST_PORT" }]}}'
# s = body.replace("$IMAGE",'nginx').replace("$CONTAINER_PORT","80").replace("$HOST_PORT","")
# print s
#
# pull_docker_image('111.231.86.41', '2376',
#                   '/images/create?fromImage=docker-registry.jdddata.com/jdddata/dac-schedule&tag=snapshot-1.0.0-81',
#                   body=None)

# container = get_container_info_by_container_name('111.231.86.41', '2376', 'dadac')
#
# print container
