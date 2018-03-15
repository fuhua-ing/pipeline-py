# -*- coding: utf-8 -*-

import os

# gocd 产生
GO_PIPELINE_NAME = os.getenv('GO_PIPELINE_NAME')
GO_JOB_NAME = os.getenv('GO_JOB_NAME')
PIPELINE_ID=os.getenv('pipelineId')

GIT_URL = os.getenv('GIT_SOURCE_URL')

GIT_BRANCH = os.getenv('GIT_BRANCH')

# nexus paramter
PROJECT_RESPOSITORY = os.getenv('PROJECT_RESPOSITORY')
CLASSIFIER = os.getenv('CLASSIFIER')
PROJECT_PACKAGE_TYPE = os.getenv('PROJECT_PACKAGE_TYPE')
GROUP_ID = os.getenv('GROUP_ID')
ARTIFACT_ID = os.getenv('ARTIFACT_ID')
PROJECT_VERSION = os.getenv('PROJECT_VERSION')

# docker paramter
DOCKER_IMAGE_NAME = os.getenv('DOCKER_IMAGE_NAME')
DOCKER_TAG_CLASSIFIER = os.getenv('DOCKER_TAG_CLASSIFIER')
DOCKER_CONTAINER_NAME = os.getenv('DOCKER_CONTAINER_NAME')

# docker paramters
PARAMTER_PORT = os.getenv('PARAMTER_PORT_LIST')
PARAMTER_VOLUME = os.getenv('PARAMTER_VOLUME_LIST')
PARAMTER_ENTRYPOINT = os.getenv('ENTRYPOINT')

# servers info
SERVER_INFO = os.getenv('SERVER_INFO')
#SERVER_PASSWD = os.getenv('SERVER_PASSWD')
