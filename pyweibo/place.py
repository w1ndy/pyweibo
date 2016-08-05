import requests
import codecs
import re

from bs4 import BeautifulSoup

from .constants import *
from .regex import *
from .fmview import FMViewParser
from .tools import parseChineseNumeric

class WeiboPlace(FMViewParser):
    def __init__(self, session, place_id):
        super().__init__(session, WEIBO_PLACE_URL.format(id=place_id))
        self._session = session
        self.id = place_id

        result = RE_PLACE_NAME.search(str(self.page))
        self.name = result.group(1)

        if not 'Pl_Core_Pt6Rank__28' in self.views:
            print(self.page.prettify)
            raise RuntimeError('cannot find corresponding nearby view')
        nearby_html = self.views['Pl_Core_Pt6Rank__28']['html']
        soup = BeautifulSoup(nearby_html, 'html.parser')
        locations = soup.find_all('a', { 'href': RE_PLACE_URL })
        self.nearby = []
        for l in locations:
            locdata = {}
            locdata['id'] = RE_PLACE_URL.match(l['href']).group(1)
            locdata['url'] = 'http://weibo.com/p/' + locdata['id']
            locdata['name'] = l.text
            locdata['weibo_count'] = parseChineseNumeric( \
                soup.find('a', { \
                    'href': 'http://weibo.com/p/' + locdata['id'] + '#feedtop' \
                }).text)
            self.nearby.append(locdata)

        map_html = self.views['Pl_Core_P5Map__21']['html']
        result = RE_PLACE_POIID.search(map_html)
        self.map_url = WEIBO_MAP_URL.format(id=result.group(1))

        r = session.get(self.map_url)
        result = RE_MAP_LNG.search(r.text)
        self.longitude = float(result.group(1))
        result = RE_MAP_LAT.search(r.text)
        self.latitude = float(result.group(1))
        result = RE_MAP_RADIUS.search(r.text)
        self.radius = float(result.group(1))

        print('%s is at (%.3f, %.3f), nearby:' % (self.name, self.latitude, self.longitude))
        print(self.nearby)
