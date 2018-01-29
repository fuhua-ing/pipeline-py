# -*- coding: utf-8 -*-
import os, re
from time import sleep
from jdd_common import GO_PIPELINE_COUNTER, GO_JOB_NAME, GO_PIPELINE_NAME, spliter, workPath, GIT_URL, GIT_BRANCH

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_last_dir(url):
    str_list = list(url)
    str_len = len(str_list)
    str_list_sub = str_list[:(str_len - 4)]
    dir = ''
    for char in str_list_sub[::-1]:
        if char != '/':
            dir = char + dir
        else:
            break
    print dir
    return dir


def pared_pom_xml(file_name):
    ns = "http://maven.apache.org/POM/4.0.0"

    tree = ET.parse(file_name)
    root = tree.getroot()

    pattern = re.compile(r'^[0-9.]+-SNAPSHOT$')

    parent = root.find("{%s}parent" % ns)
    if parent is not None:
        parent_version = parent.find("{%s}version" % ns)
        if parent_version is not None:
            text = parent_version.text
            match = pattern.match(text.strip())
            if match:
                parent_version.text = text.replace("-SNAPSHOT", "-RELEASE")

    project_version = root.find("{%s}version" % ns)
    if project_version is not None:
        text = project_version.text
        match = pattern.match(text.strip())
        if match:
            project_version.text = text.replace("-SNAPSHOT", "-RELEASE")

    properties = root.find("{%s}properties" % ns)
    if properties is not None:
        for child in properties:
            text = child.text
            match = pattern.match(text.strip())
            if match:
                child.text = text.replace("-SNAPSHOT", "-RELEASE")

    dependencies = root.find("{%s}dependencies" % ns)
    if dependencies is not None:
        for dependency in dependencies:
            version = dependency.find("{%s}version" % ns)
            if version is not None:
                text = version.text
                match = pattern.match(text.strip())
                if match:
                    version.text = text.replace("-SNAPSHOT", "-RELEASE")

    tree.write(file_name, default_namespace=ns, encoding="utf-8")


# git clone 工作目录

code_last_dir = get_last_dir(GIT_URL)

gocd_git_path = workPath + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME + spliter + 'git'

os.system('rm -rf ' + gocd_git_path)
os.system('mkdir -p ' + gocd_git_path)

print 'start to clone code'
status_git = os.system('cd ' + gocd_git_path + ' && ' + 'git clone -b ' + GIT_BRANCH + ' ' + GIT_URL)
sleep(3)
if status_git != 0:
    raise Exception('pull sourcecode from gitlab failed')

print 'end of clone code'

code_path = gocd_git_path + spliter + code_last_dir

code_release = gocd_git_path + spliter + 'release'

os.system('rm -rf ' + code_release)
os.system('mkdir -p ' + code_release)

code_release_path = code_release + spliter + code_last_dir

print 'start to find pom.xml'
p = os.popen('cd ' + code_path + ' && find ' + code_path + ' -name "pom.xml"')
str_line = list()
for line in p.readlines():
    line = line.strip()
    if not len(line):
        continue
    str_line.append(line)
print str_line
for file_name in str_line:
    pared_pom_xml(file_name)

print 'end of change snapshot'

# 本地构件通过则上传
status = os.system('cd ' + code_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean install')
sleep(3)
print 'local compiler status: ' + str(status)
if status != 0:
    raise Exception("local compiler failed")

os.system(
    'cd ' + code_path + ' && git commit -am "release" && ' + 'git tag -a ' + GIT_BRANCH + '-release ' + ' -m "release"')

status_git_push = os.system('cd ' + code_path + ' && ' + ' git push origin ' + GIT_BRANCH + '-release')
sleep(2)
if status_git_push != 0:
    raise Exception('failed to push tag to remote repository')
print 'success push tag to remote'

status_deploy = os.system(
    'cd ' + code_release + ' && ' + 'git clone -b ' + GIT_BRANCH + '-release ' + GIT_URL + ' && cd ' + code_release_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean deploy -U')
if status_deploy != 0:
    raise Exception('deploy tar.gz from tag branch code error please check')
