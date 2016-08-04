from bs4 import BeautifulSoup
import json
import re

class FMViewParser:
    def __init__(self, session, url):
        r = session.get(url)
        self.page = BeautifulSoup(r.text, 'html.parser')
        self.views = {}
        for view in filter(lambda x: x.startswith('FM.view'), \
                        map(lambda x: x.text, self.page.find_all('script'))):
            result = re.match(r'FM\.view\((.+)\);?$', view)
            if not result:
                raise RuntimeError('unexpected FM.view format!')
            cont = json.loads(result.group(1))
            self.views[cont['domid']] = cont
