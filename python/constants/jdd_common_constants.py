from python.constants.jdd_constants_from_env import GO_PIPELINE_NAME, GO_PIPELINE_COUNTER, GO_JOB_NAME, \
    DOCKER_IMAGE_NAME, DOCKER_TAG_CLASSIFIER, GIT_BRANCH

maven_url = 'maven-repository.jdddata.com'
maven_path = '/nexus/service/local/artifact/maven/redirect?' + 'r=$R' + '&g=$G' + '&a=$A' + '&v=$V' + '&c=$C' + '&p=$P'
Http_Success_code = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 300, 301, 302, 303, 304, 305, 306, 307]

spliter = '/'

DOCKER_BUILD_PATH = '/gocd-workspace/docker-build'

# docker image build path
DOCKER_BUILD_WORK_PATH = DOCKER_BUILD_PATH + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME

DOCKER_IMAGE_TAG = DOCKER_TAG_CLASSIFIER + '-' + GIT_BRANCH + '-' + GO_PIPELINE_COUNTER

CURRENT_DOCKER_WITH_TAG = DOCKER_IMAGE_NAME + ':' + DOCKER_IMAGE_TAG
