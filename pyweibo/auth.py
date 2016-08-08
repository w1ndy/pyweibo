import requests
import json
import rsa
import base64
import binascii
import codecs
import re

from random import randrange
from .constants import *

class WeiboAuthenticationError(Exception):
    def __init__(self, reason, retcode=-1, captcha_url=''):
        super(WeiboAuthenticationError, self).__init__(reason)
        self.retcode = retcode
        self.captcha_url = captcha_url

class WeiboAuthenticator:
    def __init__(self, session):
        self._session = session
        self._fetchPrelogin()

    def _fetchPrelogin(self):
        try:
            r = self._session.get(WEIBO_PRELOGIN_URL)
            self._prelogin = json.loads(r.text)
        except:
            raise

    def auth(self, username, password, captcha):
        data = {}
        if captcha:
            data['pcid'] = self._prelogin['pcid']
            data['door'] = captcha
        data['entry'] = 'weibo'
        data['gateway'] = 1
        data['from'] = ''
        data['savestate'] = 7
        data['useticket'] = 1
        data['pagerefer'] = WEIBO_LOGIN_REFERRER
        data['vsnf'] = 1
        data['su'] = codecs.decode( \
            base64.encodebytes(codecs.encode(username)), 'ascii').strip()
        data['service'] = 'miniblog'
        data['servertime'] = self._prelogin['servertime']
        data['nonce'] = self._prelogin['nonce']
        data['pwencode'] = 'rsa2'
        data['rsakv'] = self._prelogin['rsakv']
        key = rsa.PublicKey(int(self._prelogin['pubkey'], 16), 65537)
        password = codecs.encode( \
            str(data['servertime']) + '\t' + data['nonce'] + '\n' + password)
        data['sp'] = binascii.b2a_hex(rsa.encrypt(password, key))
        data['sr'] = '1920*1080'
        data['encoding'] = 'UTF-8'
        data['prelt'] = 135
        data['url'] = WEIBO_LOGIN_CALLBACK_URL
        data['returntype'] = 'META'
        try:
            r = self._session.post(WEIBO_LOGIN_URL, data=data)
        except Exception as e:
            raise WeiboAuthenticationError('login failed: ' + str(e))
        result = re.search(r'retcode=(\d+?)', r.text)
        if not result:
            raise WeiboAuthenticationError('cannot find retcode')
        retcode = int(result.group(1))
        if retcode == 0:
            result = re.search(r'replace\([\'"](.+)[\'"]\)', r.text).group(1)
            self._session.get(result)
            return
        elif retcode == 4:
            raise WeiboAuthenticationError( \
                'captcha required', 4, \
                WEIBO_CAPTCHA_IMAGE_URL.format(\
                    rand=randrange(0, 1e8), \
                    pcid=self._prelogin['pcid']))
        else:
            result = re.search(r'reason=(.+)[&\'"]', r.text)
            if not result:
                raise WeiboAuthenticationError( \
                    'login request failed', retcode)
            else:
                raise WeiboAuthenticationError( \
                    requests.utils.unquote(result.group(1), encoding='gbk'), \
                    retcode)
