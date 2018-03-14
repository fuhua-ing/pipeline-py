from python.constants.jdd_constants_from_env import GIT_URL, spliter, workPath, GO_PIPELINE_NAME, GO_PIPELINE_COUNTER, GO_JOB_NAME
from python.release.service.jdd_release_service import get_last_dir

code_last_dir = get_last_dir(GIT_URL)

gocd_git_path = workPath + spliter + GO_PIPELINE_NAME + spliter + GO_PIPELINE_COUNTER + spliter + GO_JOB_NAME + spliter + 'git'

code_path = gocd_git_path + spliter + code_last_dir

code_release = gocd_git_path + spliter + 'release'

code_release_path = code_release + spliter + code_last_dir