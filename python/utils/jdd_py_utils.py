# -*- coding: utf-8 -*-
import os


def get_os_env_exit(env):
    env_str = os.getenv(env)
    if env_str is None:
        print 'can not get Environment: ' + env
        exit(1)
    return env_str


def get_os_env(env):
    return os.getenv(env)
