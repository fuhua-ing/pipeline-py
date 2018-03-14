import os

from python.constants.jdd_constants_from_env import GIT_BRANCH, GIT_URL
from python.release.constants.jdd_release_constants import code_release, code_release_path

os.system('rm -rf ' + code_release)
os.system('mkdir -p ' + code_release)

status_deploy = os.system(
    'cd ' + code_release + ' && ' + 'git clone -b ' + GIT_BRANCH + '-release ' + GIT_URL + ' && cd ' + code_release_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean deploy -U')
if status_deploy != 0:
    raise Exception('deploy tar.gz from tag branch code error please check')
