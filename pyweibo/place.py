import requests
import codecs

from bs4 import BeautifulSoup

from .constants import *
from .fmview import FMViewParser

class WeiboPlace(FMViewParser):
    def __init__(self, session, place_id):
        super().__init__(session, WEIBO_PLACE_URL.format(id=place_id))
        self._session = session
        print(self.views.keys())
