import yaml


class Settings(object):
    def __init__(self, yaml_file):
        self.file = yaml_file
        self.data = self._load_config(yaml_file)

    def get(self, *keys):
        _element = self.data
        for key in keys:
            if key not in _element:
                raise Exception(f'{key} not found. Please add it to the YAML config file')
            _element = _element[key]
        return _element

    @staticmethod
    def _load_config(file: str):
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
        return data
