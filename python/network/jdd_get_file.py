# -*- coding: utf-8 -*-
import urllib2, time

maven_url = 'maven-repository.jdddata.com'
maven_path = '/nexus/service/local/artifact/maven/redirect?' + 'r=$R' + '&g=$G' + '&a=$A' + '&v=$V' + '&c=$C' + '&p=$P'
Success_Http_Code = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]


def get_tar(r, g, a, v, c, p, curr_path):
    url = maven_path.replace("$R", r).replace("$G", g).replace("$A", a).replace("$V", v).replace("$C", c).replace("$P",
                                                                                                                  p)
    url = 'https://' + maven_url + url
    print 'get artifact url: ' + url
    resp = urllib2.urlopen(url, timeout=30000)
    print resp.code
    true_url = resp.geturl()
    print true_url
    time.sleep(2)
    f = urllib2.urlopen(true_url, timeout=300000)
    http_code = f.code
    print http_code
    data = f.read()
    with open(curr_path + '/' + 'app-install.tar.gz', "wb") as code:
        code.write(data)
    time.sleep(5)
    md5 = urllib2.urlopen(true_url + '.md5', timeout=30000)
    if md5.code not in Success_Http_Code:
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

# path = '.'
# get_tar('public', 'com.jdddata.crawler', 'crawler-project-transfermarkt', '2.0.1-SNAPSHOT', 'install', 'tar.gz', path)
