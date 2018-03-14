import os
from time import sleep

from python.jdd_common import GIT_BRANCH
from python.release.service.jdd_release_service import code_path

os.system(
    'cd ' + code_path + ' && git commit -am "release" && ' + 'git tag -a ' + GIT_BRANCH + '-release ' + ' -m "release"')

status_git_push = os.system('cd ' + code_path + ' && ' + ' git push origin ' + GIT_BRANCH + '-release')
sleep(2)
if status_git_push != 0:
    raise Exception('failed to push tag to remote repository')
print 'success push tag to remote'
