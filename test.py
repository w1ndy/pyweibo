from pyweibo import SinaWeibo

import json

with open('config.json', 'r') as f:
    config = json.loads(f.read())

cred = config['credentials']
w = SinaWeibo()
captcha_img = w.login(cred['username'], cred['password'])
if captcha_img:
    captcha_img.show()
    captcha = input('Captcha Code: ')
    w.login(cred['username'], cred['password'], captcha)

place = w.getPlaceById(config['tests']['place_id'])
