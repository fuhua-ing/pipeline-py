# 本地构件通过则上传
import os
from time import sleep

from python.release.jdd_release_common import code_path

status = os.system('cd ' + code_path + ' && ' + '/usr/local/apache-maven-3.5.0/bin/mvn clean install -U')
sleep(3)
print 'local compiler status: ' + str(status)
if status != 0:
    raise Exception("local compiler failed")
