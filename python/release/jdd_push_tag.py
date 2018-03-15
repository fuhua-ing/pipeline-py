import os
from time import sleep

from constants.jdd_constants_from_env import GIT_BRANCH
from constants.jdd_release_constants import code_path

os.system(
    'cd ' + code_path + ' && git add . && git commit -m "release" && ' + 'git tag -a ' + GIT_BRANCH + '-release ' + ' -m "release"')

status_git_push = os.system('cd ' + code_path + ' && ' + ' git push origin ' + GIT_BRANCH + '-release')
sleep(2)
if status_git_push != 0:
    raise Exception('failed to push tag to remote repository')
print 'success push tag to remote'
