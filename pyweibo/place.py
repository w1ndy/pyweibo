import requests
import codecs
import re

from bs4 import BeautifulSoup

from .constants import *
from .fmview import FMViewParser

class WeiboPlace(FMViewParser):
    def __init__(self, session, place_id):
        super().__init__(session, WEIBO_PLACE_URL.format(id=place_id))
        self._session = session

        result = re.search(r'\[["\']onick["\']\]=["\'](.+)["\'];', \
            str(self.page))
        self.name = result.group(1)

        nearby_html = self.views['Pl_Core_Pt6Rank__28']['html']
        soup = BeautifulSoup(nearby_html, 'html.parser')
        locations = soup.find_all('a', \
            { 'href': re.compile(r'^http://weibo\.com/p/\w+\?') })
        self.nearby = []
        for l in locations:
            locdata = {}
            locdata['id'] = re.match( \
                r'http://weibo\.com/p/(\w+)', l['href']).group(1)
            locdata['url'] = 'http://weibo.com/p/' + locdata['id']
            locdata['name'] = l.text
            locdata['weibo_count'] = int(soup.find('a', \
                { 'href': 'http://weibo.com/p/' + locdata['id'] + '#feedtop' }).text)
            self.nearby.append(locdata)

        map_html = self.views['Pl_Core_P5Map__21']['html']
        result = re.search(r'poiid=([\d\.]+)_([\d\.]+)&', map_html)
        self.longitude = float(result.group(1))
        self.latitude = float(result.group(2))
        print('%s is at (%.3f, %.3f), nearby:' % (self.name, self.latitude, self.longitude))
        print(self.nearby)
