# -*- coding: utf-8 -*-
import os, re
from jdd_common import GO_PIPELINE_COUNTER, GO_JOB_NAME, GO_PIPELINE_NAME, spliter, workPath, SOURCE_CODE_URL, BRANCH

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

code_last_dir = get_last_dir(SOURCE_CODE_URL)

gocd_git_path = workPath + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME

gocd_git_path_release = gocd_git_path + spliter + 'release'

status_git = os.system('cd ' + gocd_git_path + ' && ' + 'git clone -b ' + BRANCH + ' ' + SOURCE_CODE_URL)
if status_git != 0:
    raise Exception('pull sourcecode from gitlab failed')

code_path = gocd_git_path + spliter + code_last_dir

p = os.popen('cd ' + code_path + ' && find ' + code_path + ' -name "pom.xml')
str_line = list()
for line in p.readlines():
    line = line.strip()
    if not len(line):
        continue
    str_line.append(line)

for file_name in str_line:
    pared_pom_xml(file_name)

# 本地构件通过则上传
status = os.system('cd ' + code_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean install')
print 'local compiler status: ' + status
if status != 0:
    raise Exception("local compiler failed")

os.system('cd ' + code_path + ' && ' + 'git tag -a ' + BRANCH + '-release ' + ' -m "release"')

status_git_push = os.system('cd ' + code_path + ' && ' + ' git push origin ' + BRANCH + '-release')
if status_git_push != 0:
    raise Exception('failed to push tag to remote repository')
print 'success push tag to remote'

status_deploy = os.system(
    'cd ' + gocd_git_path_release + ' && ' + 'git clone -b ' + BRANCH + '-release ' + SOURCE_CODE_URL + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean deploy -U')
if status_deploy != 0:
    raise Exception('deploy tar.gz from tag branch code error please check')
