import requests
import json
import rsa
import base64
import binascii
import codecs
import re

_ImageSupport = True
try:
    from PIL import Image
    from io import BytesIO
except:
    _ImageSupport = False
    print('cannot find library pillow, image support is turned off.')

from .constants import *
from .auth import WeiboAuthenticator, WeiboAuthenticationError
from .place import WeiboPlace

class SinaWeibo:
    def __init__(self):
        self._signed_in = False
        self._session = requests.Session()
        self._session.headers.update({'User-Agent': USER_AGENT})
        self._auth = WeiboAuthenticator(self._session)

    def login(self, username, password, captcha=None):
        if self._signed_in:
            raise RuntimeError('already signed in')
        try:
            self._auth.auth(username, password, captcha)
        except WeiboAuthenticationError as e:
            if e.retcode == 4 and _ImageSupport:
                r = self._session.get(e.captcha_url)
                i = Image.open(BytesIO(r.content))
                return i
            else:
                raise
        return None

    def getPlaceById(self, id):
        return WeiboPlace(self._session, id)
