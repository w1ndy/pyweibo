from pyweibo import SinaWeibo

import json

with open('config.json', 'r') as f:
    config = json.loads(f.read())
    cred = config['credentials']
    w = SinaWeibo()
    w.login(cred['username'], cred['password'])
