from pyweibo import SinaWeibo

import json

with open('config.json', 'r') as f:
    config = json.loads(f.read())
    cred = config['credentials']
    http = config['http']

w = SinaWeibo()
w.getSession().setThrottle(http['request_interval'])
w.getSession().setRequestTimeout(http['timeout'])
w.getSession().setMaxRetries(http['max_retries'])

captcha_img = w.login(cred['username'], cred['password'])
if captcha_img:
    captcha_img.show()
    captcha = input('Captcha Code: ')
    w.login(cred['username'], cred['password'], captcha)
