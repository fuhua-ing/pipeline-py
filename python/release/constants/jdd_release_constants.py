from jdd_constants_from_env import GIT_URL, GO_PIPELINE_NAME, GO_JOB_NAME
from jdd_release_service import get_last_dir

spliter = '/'

GIT_CODE_PATH = '/gocd-workspace/git-code'

code_last_dir = get_last_dir(GIT_URL)

gocd_git_path = GIT_CODE_PATH + spliter + code_last_dir + spliter + 'git'

code_path = gocd_git_path + spliter + code_last_dir

code_release = gocd_git_path + spliter + 'release'

code_release_path = code_release + spliter + code_last_dir
