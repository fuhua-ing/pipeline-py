# -*- coding: utf-8 -*-
from utils.jdd_py_utils import get_os_env_exit, get_os_env

spliter = '/'

workPath = '/gocd-workspace/docker-build'

# gocd 产生
GO_PIPELINE_NAME = get_os_env_exit('GO_PIPELINE_NAME')
GO_PIPELINE_COUNTER = get_os_env_exit('GO_PIPELINE_COUNTER')
GO_JOB_NAME = get_os_env_exit('GO_JOB_NAME')

# pipeline env
SOURCE_CODE_URL = get_os_env('GIT_URL')

# stage env
BRANCH = get_os_env('GIT_BRANCH')
