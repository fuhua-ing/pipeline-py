# -*- coding: utf-8 -*-
import os
import urllib2
from time import sleep

from jdd_common_constants import maven_path, maven_url, Http_Success_code



def getCounterCode(url, pipelineId):
    resp = urllib2.urlopen(url + '?pipelineId=' + pipelineId)
    print resp.code
    data = resp.read()
    print 'The counter num is :'
    print data
    return data

def get_tar(r, g, a, v, c, p, curr_path):
    url = maven_path.replace("$R", r).replace("$G", g).replace("$A", a).replace("$V", v).replace("$C", c).replace("$P",
                                                                                                                  p)
    url = 'https://' + maven_url + url
    print 'get artifact url: ' + url
    resp = urllib2.urlopen(url, timeout=30000)
    print resp.code
    true_url = resp.geturl()
    print true_url
    sleep(2)
    f = urllib2.urlopen(true_url, timeout=300000)
    http_code = f.code
    print http_code
    data = f.read()
    with open(curr_path + '/' + 'app-install.tar.gz', "wb") as code:
        code.write(data)
    sleep(5)
    md5 = urllib2.urlopen(true_url + '.md5', timeout=30000)
    if md5.code not in Http_Success_code:
        return "-1"
    md5_code = md5.read()
    print md5_code
    return md5_code


def get_dockerfile(curr_path):
    url = 'https://gitlab.jdddata.com/gezhiwei/dockerfile-collection/raw/master/dac/Dockerfile?private_token=3UQ39VW441S3apUWNbRk'
    resp = urllib2.urlopen(url, timeout=30000)
    print 'get dockerfile http code: ' + str(resp.code)
    data = resp.read()
    with open(curr_path + '/' + 'Dockerfile', "wb") as code:
        code.write(data)
    print 'end of get Dockerfile'


def get_tar_md5(curr_path):
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
