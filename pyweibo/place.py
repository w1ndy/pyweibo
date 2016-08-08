import requests
import codecs
import re
import json

from bs4 import BeautifulSoup

from .constants import *
from .regex import *
from .fmview import FMViewParser
from .tools import parseChineseNumeric, retryUntil
from .tweet import WeiboTweet

class LocationWeiboTweet(WeiboTweet):
    def __init__(self, session, place):
        pass

class WeiboPlace(FMViewParser):
    def __init__(self, session, place_id):
        super().__init__(session, WEIBO_PLACE_URL.format(id=place_id))
        self._session = session
        self.id = place_id

        def _readNameAndWeiboCount():
            result = RE_PLACE_NAME.search(str(self.page))
            self.name = result.group(1)
            result = RE_PLACE_WEIBO_COUNT.search( \
                self.views['Pl_Third_App__17']['html'])
            self.weibo_count = result.group(1)
        retryUntil(_readNameAndWeiboCount, retry_func=self.reload)

        self._visited_type_parser = {}
        self._retrieveLocation()

        print('%s is at (%.3f, %.3f)' % \
            (self.name, self.latitude, self.longitude))

    def queryNearby(self):
        _visited_poi_set = set()
        nearby_queue = []

        def _readNearby():
            nonlocal nearby_queue
            nearby_queue = self._parseNearbyPage( \
                self.views['Pl_Core_Pt6Rank__28']['html'])
        retryUntil(_readNearby, retry_func=self.reload)
        while nearby_queue:
            loc = nearby_queue.pop()
            _visited_poi_set.add(loc['id'])
            yield loc

        for t in WEIBO_POI_CLASS:
            url = WEIBO_POILIST_URL.format(id=self.id, tid=t)

            def _readNearbyFromClass():
                nonlocal nearby_queue
                if url in self._visited_type_parser:
                    parser = self._visited_type_parser[url]
                else:
                    parser = FMViewParser(self._session, url)
                nearby_queue = self._parseNearbyPage( \
                    parser.views['Pl_Core_Pt6Rank__28']['html'])

            def _retryPageFetch():
                self._visited_type_parser[url] = \
                    FMViewParser(self._session, url)

            retryUntil(_readNearbyFromClass, retry_func=_retryPageFetch)

            while nearby_queue:
                loc = nearby_queue.pop()
                if loc['id'] in _visited_poi_set: continue
                _visited_poi_set.add(loc['id'])
                yield loc

    def _parseNearbyPage(self, page):
        nearby = []
        soup = BeautifulSoup(page, 'html.parser')
        locations = soup.find_all('a', { 'href': RE_PLACE_URL })
        for l in locations:
            locdata = {}
            locdata['id'] = RE_PLACE_URL.match(l['href']).group(1)
            locdata['url'] = 'http://weibo.com/p/' + locdata['id']
            locdata['name'] = l.text
            locdata['weibo_count'] = parseChineseNumeric( \
                soup.find('a', { \
                    'href': 'http://weibo.com/p/' + locdata['id'] + '#feedtop' \
                }).text)
            nearby.append(locdata)
        return nearby

    def _retrieveLocation(self):
        def _readPoiId():
            map_html = self.views['Pl_Core_P5Map__21']['html']
            result = RE_PLACE_POIID.search(map_html)
            self.map_url = WEIBO_MAP_URL.format(id=result.group(1))
        retryUntil(_readPoiId, retry_func=self.reload)

        r = None
        def _getMapPage():
            nonlocal r
            r = self._session.get(self.map_url)
        def _resolveGeoInfo():
            result = RE_MAP_LNG.search(r.text)
            self.longitude = float(result.group(1))
            result = RE_MAP_LAT.search(r.text)
            self.latitude = float(result.group(1))
            result = RE_MAP_RADIUS.search(r.text)
            self.radius = float(result.group(1))
        _getMapPage()
        retryUntil(_resolveGeoInfo, retry_func=_getMapPage)
