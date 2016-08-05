import json
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

class ExampleConfig:
    def __init__(self, path_to_conf):
        f = open(path_to_conf, 'r')
        self._config = json.loads(f.read())
        self.cred = self._config['credentials']
        self.http = self._config['http']
