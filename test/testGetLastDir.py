from python.release.service.jdd_release_service import get_last_dir

url = 'https://gitlab.jdddata.com/project/dac/dac.git'
print get_last_dir(url=url)