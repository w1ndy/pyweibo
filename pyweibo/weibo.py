import requests
import json
import rsa
import base64
import binascii
import codecs
import re

from .constants import *
from .auth import WeiboAuthenticator

class SinaWeibo:
    def __init__(self):
        self._signed_in = False
        self._session = requests.Session()
        self._session.headers.update({'User-Agent': USER_AGENT})
        self._auth = WeiboAuthenticator(self._session)

    def login(self, username, password):
        if self._signed_in:
            raise RuntimeError('already signed in')
        self._auth.auth(username, password)
        return True
