import os
from typing import Tuple

import toml
from sanic_envconfig import EnvConfig


app_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(app_dir, os.pardir))
pyproject_info = toml.load(os.path.join(project_root, 'pyproject.toml'))
poetry_info = pyproject_info['tool']['poetry']

app_name = poetry_info["name"].lower()
service_name = f'{app_name}'

default_ip = '0.0.0.0'


class Config(EnvConfig):
    SERVER_IP: str = default_ip
    SERVER_PORT: int = 80
    PG_CONNECTION: str = None
    APP_DIR: str = app_dir
    PROJECT_ROOT: str = project_root
    DDTARCE_HOSTNAME: str = 'localhost'
    IS_DOCKER: bool = False
    DEBUG: bool = False
    APP_NAME: str = app_name
    SERVICE_NAME: str = service_name
    API_TITLE: str = service_name.title()
    API_VERSION: str = poetry_info['version']
    API_DESCRIPTION: str = poetry_info['description']
    API_SCHEMES: Tuple[str] = ('http', 'https')
    CORS_AUTOMATIC_OPTIONS: bool = True
    CORS_SUPPORTS_CREDENTIALS: bool = True
    CORS_ORIGINS: Tuple[str] = ('.*',)
    CORS_SEND_WILDCARD: bool = False
