import re

RE_PLACE_NAME = re.compile(r'\[["\']onick["\']\]=["\'](.+)["\'];')
RE_PLACE_URL = re.compile(r'^http://weibo\.com/p/(\w+)\?')
RE_PLACE_POIID = re.compile(r'poiid=(.+?)[\?"&]')
RE_MAP_URL = re.compile(r'(http://place\.weibo\.com/.+?)"')
RE_MAP_LNG = re.compile(r'poiObject\.lon = ([\d\.]+?);')
RE_MAP_LAT = re.compile(r'poiObject\.lat = ([\d\.]+?);')
RE_MAP_RADIUS = re.compile(r'\$radius = ([\d\.]+?);')
