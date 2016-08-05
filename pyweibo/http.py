import requests
import time
import re

_UnixSignalSupport = True
try:
    import signal
except:
    _UnixSignalSupport = False
    print('no signal support on this platform, timeout will be disabled.')

from .constants import USER_AGENT, WEIBO_REJECTED_ERROR

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

    def _tryUntilSucceed(self, func, validate=None):
        left_retries = self._max_retries
        result = None
        while left_retries > 0:
            left_retries -= 1
            try:
                if _UnixSignalSupport:
                    def sighandler(signum, frame):
                        raise RuntimeError('timed out')
                    signal.signal(signal.SIGALRM, sighandler)
                    signal.alarm(self._request_timeout)
                result = func()
                if validate and not validate(result):
                    raise RuntimeError('HTTPSession: validation error')
                if _UnixSignalSupport:
                    signal.alarm(0)
                break
            except Exception as e:
                if _UnixSignalSupport:
                    signal.alarm(0)
                if left_retries:
                    print('[%d/%d] Exception: %s' % ( \
                        self._max_retries - left_retries, \
                        self._max_retries, \
                        str(e)))
                    time.sleep(self._request_min_interval)
                else:
                    raise
        return result

    def _validateHttpResponse(self, r):
        if r.status_code >= 400:
            return False
        if re.search(WEIBO_REJECTED_ERROR, r.text):
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
