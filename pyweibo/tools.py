import time

_UnixSignalSupport = True
def _retryTimeoutSignalHandler(signum, frame):
    raise RuntimeError('timed out')

try:
    import signal
    signal.signal(signal.SIGALRM, _retryTimeoutSignalHandler)
except:
    _UnixSignalSupport = False
    print('no signal support on this platform, timeout will be disabled.')

NUMERIC_MAP = {
    '\u5341': 10,
    '\u767e': 100,
    '\u5343': 1000,
    '\u4e07': 10000,
    '\u4ebf': 100000000
}

def parseChineseNumeric(s):
    base = 1
    while len(s):
        if s[-1] in NUMERIC_MAP:
            base *= NUMERIC_MAP[s[-1]]
            s = s[:-1]
        else:
            return base * float(s)
    return base


def retryUntil(func, validator=None, retry_func=None, max_retries=3, \
        timeout=15, wait=0):
    left_retries = max_retries
    result = None
    while left_retries > 0:
        left_retries -= 1
        try:
            if _UnixSignalSupport:
                signal.alarm(timeout)
            result = func()
            if _UnixSignalSupport:
                signal.alarm(0)
            if validator and not validator(result):
                raise RuntimeError('validation error')
            break
        except Exception as e:
            if _UnixSignalSupport:
                signal.alarm(0)
            if left_retries:
                print('[%d/%d] Exception: %s' % ( \
                    max_retries - left_retries, \
                    max_retries, \
                    str(e)))
                if retry_func: retry_func()
                if wait: time.sleep((max_retries - left_retries) * wait)
            else:
                raise
    return result
