import requests
import json
import rsa
import base64
import binascii
import codecs
import re

from .constants import *

class WeiboAuthenticator:
    def __init__(self, session):
        self._session = session
        try:
            r = self._session.get(WEIBO_PRELOGIN_URL, \
                    headers={'User-Agent': USER_AGENT})
            self._prelogin = json.loads(r.text)
        except e:
            raise RuntimeError('unable to parse prelogin data!')

    def auth(self, username, password):
        data = {}
        data['entry'] = 'weibo'
        data['gateway'] = 1
        data['from'] = ''
        data['savestate'] = 7
        data['useticket'] = 1
        data['pagerefer'] = WEIBO_LOGIN_REFERRER
        data['vsnf'] = 1
        data['su'] = codecs.decode( \
            base64.encodebytes(codecs.encode(username)), \
            encoding='ascii').strip()
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
            raise RuntimeError('login failed: ' + str(e))
        result = re.search(r'retcode=(\d+?)', r.text)
        if not result:
            raise RuntimeError('cannot find retcode')
        retcode = result.group(1)
        if int(retcode) != 0:
            result = re.search(r'reason=(.+)[&\'"]', r.text)
            if not result:
                raise RuntimeError('login request failed with ' + str(retcode))
            else:
                raise RuntimeError('login request failed with ' + \
                    str(retcode) + ': ' + \
                    requests.utils.unquote(result.group(1), encoding='gbk'))
