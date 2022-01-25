from pkg_resources import resource_filename
from yaml import safe_load, safe_dump
from json import dumps, loads
from ocrd_validators.json_validator import JsonValidator

with open(resource_filename(__name__, 'config.schema.yml')) as _f:
    config_schema = safe_load(_f)

class OcrmultievalConfig():

    def __init__(self, config):
        with open(config if config else resource_filename(__name__, 'default_config.yml'), 'r') as f:
            self._config = safe_load(f)

    def get(self, backend, fallback):
        return getattr(self._config, backend, fallback)

    def dump(self, fmt):
        return dumps(self._config, indent=4) if fmt == 'json' else safe_dump(self._config)

    def validate(self):
        return JsonValidator.validate(self._config, config_schema)
