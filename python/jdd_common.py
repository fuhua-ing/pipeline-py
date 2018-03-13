# -*- coding: utf-8 -*-

import os

spliter = '/'

workPath = '/gocd-workspace/docker-build'

# gocd 产生
GO_PIPELINE_NAME = os.getenv('GO_PIPELINE_NAME')
GO_PIPELINE_COUNTER = os.getenv('GO_PIPELINE_COUNTER')
GO_JOB_NAME = os.getenv('GO_JOB_NAME')

# pipeline env
GIT_URL = os.getenv('GIT_SOURCE_URL')

# stage env
GIT_BRANCH = os.getenv('GIT_BRANCH')

# job env
# nexus paramter
PROJECT_RESPOSITORY = os.getenv('PROJECT_RESPOSITORY')
CLASSIFILER = os.getenv('CLASSIFILER')
PROJECT_PACKAGE_TYPE = os.getenv('PROJECT_PACKAGE_TYPE')
GROUP_ID = os.getenv('GROUP_ID')
ARTIFACT_ID = os.getenv('ARTIFACT_ID')
PROJECT_VERSION = os.getenv('PROJECT_VERSION')
#
# docker paramter
DOCKER_IMAGE_NAME = os.getenv('DOCKER_IMAGE_NAME')
DOCKER_TAG_VERSION = os.getenv('DOCKER_TAG_VERSION')
DOCKER_CONTAINER_NAME = os.getenv('DOCKER_CONTAINER_NAME')

# wait to classfiler


PARAMTER_PORT = os.getenv('PARAMTER_PORT_LIST')

PARAMTER_VOLUME = os.getenv('PARAMTER_VOLUME_LIST')

PARAMTER_ENTRYPOINT = os.getenv('ENTRYPOINT')