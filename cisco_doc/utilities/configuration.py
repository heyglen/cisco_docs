
import os
import copy
import base64
import logging
import pathlib

import appdirs
import yaml
import click

from .dot_dict import DotDict

MODULE_NAME = __name__.split('.')[0].lower()
APP_AUTHOR = 'heyglen'
KEYRING_DOMAIN = MODULE_NAME.lower()
ENVIRONMENT_VARIABLES = os.environ.copy()

logger = logging.getLogger(__name__)

default_configuration = {
    'log': {
        'level': 'debug',
    },
}


def _get_env(name, cls_type=str, decode=False):
    value = ENVIRONMENT_VARIABLES.get(name)
    if value and cls_type is not None:
        value = cls_type(value)
    if isinstance(value, str) and decode:
        value = base64.b64decode(value)
        if value is not None:
            value = value.decode('utf8')
    if value is not None:
        if decode:
            logger.debug(f'Loaded environment vairable {name}')
        else:
            logger.debug(f'Loaded environment vairable {name}={value}')
    return value


def _clean_config(config):
    """ Remove any environment variables that are not set """
    new_dict = dict()
    for key, value in config.items():
        if isinstance(value, dict):
            value = _clean_config(value)
            if value:
                new_dict[key] = value
        elif value is not None:
            new_dict[key] = value
    return new_dict

configuration = copy.deepcopy(default_configuration)

configuration_directory = pathlib.Path(appdirs.user_config_dir(
    MODULE_NAME,
    APP_AUTHOR
))
configuration_path = configuration_directory / 'configuration.yml'

if configuration_directory.is_dir():
    if configuration_path.is_file():
        with open(configuration_path) as f:
            loaded_config = yaml.safe_load(f) or dict()
            loaded_config = _clean_config(loaded_config)
            configuration.update(loaded_config)
            logger.debug(f'Loaded configuration file {configuration_path}')

            if configuration['credentials']['password']:
                configuration['credentials']['password'] = base64.b64decode(
                    configuration['credentials']['password']
                ).decode('utf8').strip()

environment_variables = _clean_config({
    'log': {
        'level': _get_env('cisco_doc_LOG_LEVEL'),
    },
})

configuration.update(environment_variables)

configuration['log']['level'] = getattr(logging, configuration['log']['level'].upper())

configuration = DotDict(configuration)