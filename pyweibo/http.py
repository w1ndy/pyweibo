import requests
import time
import re

from .tools import retryUntil
from .constants import USER_AGENT, WEIBO_REJECTED_ERROR, WEIBO_NOTFOUND_ERROR

class HTTPSession:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({ 'User-Agent': USER_AGENT })
        self._request_min_interval = 0
        self._max_retries = 3
        self._request_timeout = 15
        self._wait_after_rejection = 3
        self._last_request_timestamp = time.clock()

    def _doThrottle(self):
        dt = time.clock() - self._last_request_timestamp
        if dt > 0.001 and dt < self._request_min_interval:
            print('warning: throttling request, sleep %f sec' % dt)
            time.sleep(dt)

    def _tryUntilSucceed(self, func, validator=None):
        return retryUntil(func, \
            validator=validator, \
            max_retries=self._max_retries, \
            timeout=self._request_timeout, \
            wait=self._request_min_interval)

    def _validateHttpResponse(self, r):
        if r.status_code >= 400:
            return False
        if re.search('(%s)|(%s)' % \
                (WEIBO_REJECTED_ERROR, WEIBO_NOTFOUND_ERROR), r.text):
            print('rejected by server, waiting...')
            time.sleep(self._wait_after_rejection)
            return False
        return True

    def get(self, *kargs, **kwargs):
        def _delegatedGet():
            r = self._session.get(*kargs, **kwargs)
            self._last_request_timestamp = time.clock()
            return r
        self._doThrottle()
        return self._tryUntilSucceed(_delegatedGet, self._validateHttpResponse)

    def post(self, *kargs, **kwargs):
        def _delegatedPost():
            r = self._session.post(*kargs, **kwargs)
            self._last_request_timestamp = time.clock()
            return r
        self._doThrottle()
        return self._tryUntilSucceed(_delegatedPost, self._validateHttpResponse)

    def setThrottle(self, sec):
        self._request_min_interval = sec

    def setRequestTimeout(self, sec):
        self._request_timeout = sec

    def setMaxRetries(self, times):
        self._max_retries = times
