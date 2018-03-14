import re

from python.jdd_common import GIT_URL, spliter, workPath, GO_PIPELINE_NAME, GO_PIPELINE_COUNTER, GO_JOB_NAME

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


code_last_dir = get_last_dir(GIT_URL)

gocd_git_path = workPath + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME + spliter + 'git'

code_path = gocd_git_path + spliter + code_last_dir

code_release = gocd_git_path + spliter + 'release'

code_release_path = code_release + spliter + code_last_dir
