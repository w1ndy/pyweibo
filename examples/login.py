import config

from pyweibo import SinaWeibo

def doInteractiveLogin():
    c = config.ExampleConfig('../config.json')

    w = SinaWeibo()
    w.getSession().setThrottle(c.http['request_interval'])
    w.getSession().setRequestTimeout(c.http['timeout'])
    w.getSession().setMaxRetries(c.http['max_retries'])

    captcha_img = w.login(c.cred['username'], c.cred['password'])
    if captcha_img:
        captcha_img.show()
        captcha = input('Captcha Code: ')
        w.login(c.cred['username'], c.cred['password'], captcha)

    return w, c

if __name__ == '__main__':
    doInteractiveLogin()
