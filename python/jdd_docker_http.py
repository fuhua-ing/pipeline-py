# -*- coding: utf-8 -*-
import httplib, socket, ssl, traceback, json
from _ssl import PROTOCOL_TLSv1_2

Http_Success_code = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]

ca_cert_file = '/opt/test_std/cert/ca.pem'
key_file = '/opt/test_std/cert/key.pem'
cert_file = '/opt/test_std/cert/cert.pem'

container_info_all = '/containers/json?all=1'
container_stop = '/containers/{0}/stop'
container_delete = '/containers/{0}'
container_create = '/containers/create?name={0}'

image_pull = '/images/create?fromImage={0}&tag={1}'

socket.setdefaulttimeout(12000)


def del_last_char(str):
    str_list = list(str)
    str_list.pop()
    return "".join(str_list)


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
            return 'time_out'
        else:
            res_json = json.loads(http_resp)
            for container in res_json:
                container_name_list = container['Names']
                container_name = container_name_list[0]
                if container_name == ('/' + name):
                    return container
                else:
                    return "!exsit"
    except Exception:
        print traceback.format_exc()
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


def create_container(host, port, docker_container_name, current_docker, paramter_port, paramter_volume):
    try:
        httpsConn = httplib.HTTPSConnection(host, port)
        sock = socket.create_connection((httpsConn.host, httpsConn.port))
        httpsConn.sock = ssl.wrap_socket(sock, key_file, cert_file, cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=PROTOCOL_TLSv1_2,
                                         ca_certs=ca_cert_file)
        # body = '{"Image":"$IMAGE","PortBindings": { "$CONTAINER_PORT/tcp": [{ "HostPort": "$HOST_PORT" }]}}'
        # body = '{"Image":"docker-registry.jdddata.com/jdddata/dac-schedule:snapshot-1.0.0-81" , "HostConfig":{"Binds":["/root/gezhiwei/log:/usr/local/app/log"]}}'


        body = '{"Image":' + '"' + current_docker + '"'
        if paramter_port is not None and len(paramter_port) > 0:
            body = body + ',' + '"PortBindings":{'
            p = ''
            for port in paramter_port:
                li = str(port).split(":")
                p = p + '"' + li[0] + '/tcp' + '":[{"HostPort":"' + '"' + li[1] + '"}]' + ","
            p = del_last_char(p) + '}'
            body = body + p

        if paramter_volume is not None:
            body = body + ',' + '"HostConfig":{"Binds":['
            body = body + '"' + paramter_volume + '"]}'

        body = body + '}'

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
container = get_container_info_by_container_name('192.168.136.81', '2376', "modest_jepsen")
print type(container)
print container
