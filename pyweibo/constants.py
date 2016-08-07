WEIBO_PRELOGIN_URL = \
    'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=MTg2Njc5MzY5MjA%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1470199107549'

WEIBO_LOGIN_REFERRER = \
    'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F'

WEIBO_LOGIN_CALLBACK_URL = \
    'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'

WEIBO_LOGIN_URL = \
    'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

WEIBO_CAPTCHA_IMAGE_URL = \
    'http://login.sina.com.cn/cgi/pin.php?r={rand}&s=0&p={pcid}'

WEIBO_PLACE_URL = 'http://weibo.com/p/{id}/home'

WEIBO_MAP_URL = \
    'http://place.weibo.com/index.php?_p=place_page&_a=poi_map_right&poiid={id}'

WEIBO_REJECTED_ERROR = \
    '\u4f60\u8bbf\u95ee\u7684\u9875\u9762\u5730\u5740\u6709\u8bef'

WEIBO_NOTFOUND_ERROR = \
    '\u6682\u65f6\u6ca1\u6709\u5185\u5bb9\u54e6'

WEIBO_POILIST_URL = \
    'http://weibo.com/p/{id}/home?pids=Pl_Core_Pt6Rank__28&cfs=300&Pl_Core_Pt6Rank__28_filter=filter%3D{tid}&ajaxpagelet=1&ajaxpagelet_v6=1'

WEIBO_LOCATION_TWEETS_URL = \
    'http://weibo.com/p/{id}/home?pids=Pl_Third_App__17&since_id=&page={page}&ajaxpagelet=1&ajaxpagelet_v6=1'

WEIBO_LOCATION_TWEETS_AJAX_URL = \
    'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100101&current_page=64&since_id=&page=22&pagebar=0&tab=home&pl_name=Pl_Third_App__17&id=100101B2094750DA6DA6FC409E&script_uri=/p/100101B2094750DA6DA6FC409E/home&feed_type=1&pre_page=22&domain_op=100101&__rnd=1470450242828'

WEIBO_POI_CLASS = ['64', '44', '19', '51', '115', '194', '169', '258']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
