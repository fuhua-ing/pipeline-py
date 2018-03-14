from python.constants.jdd_common_constants import CURRENT_DOCKER_WITH_TAG

C_docker_build = 'docker build -t ' + CURRENT_DOCKER_WITH_TAG + ' .'
C_docker_push = 'docker push ' + CURRENT_DOCKER_WITH_TAG
C_docker_rm_local = 'docker rmi ' + CURRENT_DOCKER_WITH_TAG
