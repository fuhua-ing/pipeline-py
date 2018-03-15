# -*- coding: utf-8 -*-
import os
from time import sleep

from constants.jdd_constants_from_env import GIT_URL, GIT_BRANCH
from constants.jdd_release_constants import gocd_git_path

os.system('rm -rf ' + gocd_git_path)
os.system('mkdir -p ' + gocd_git_path)

print 'start to clone code'
status_git = os.system('cd ' + gocd_git_path + ' && ' + 'git clone -b ' + GIT_BRANCH + ' ' + GIT_URL)
sleep(3)
if status_git != 0:
    raise Exception('pull sourcecode from gitlab failed')

print 'end of clone code'
