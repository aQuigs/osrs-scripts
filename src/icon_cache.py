import json

from pyquery import PyQuery
from urllib.parse import quote_plus as url_encode
from urllib.request import Request, urlopen

WIKI_URL_BASE='https://oldschool.runescape.wiki'
LOOKUP_SUFFIX='/w/Special:Lookup'

ICON_OVERRIDES = {
    '24868': '11810', # Golden AGS -> Arma hilt
    '24869': '11812', # Golden BGS -> Bandos hilt
    '24870': '11814', # Golden SGS -> Sara hilt
    '24871': '11816', # Golden ZGS -> Zamorak hilt
}


class IconCache:
    def __init__(self, filename):
        self.cache = self._read_cache(filename)
        self.filename = filename

    def get(self, name, id):
        if id not in self.cache:
            self.cache[id] = self._find_url(name, id)
            self._flush()

        return self.cache[id]

    def _find_url(self, name, id):
        icon_id = ICON_OVERRIDES.get(id, id)
        search_url=f"{WIKI_URL_BASE}{LOOKUP_SUFFIX}?type=item&id={icon_id}&name={url_encode(name)}"

        print(f"Finding icon for {name=} {id=} {icon_id=}..")

        wiki_page = urlopen(Request(
            search_url,
            headers={'User-Agent' : "Magic Browser"}
        )).read()

        pq = PyQuery(wiki_page)
        img_src = pq('.inventory-image>a:last-child>img').attr('src')

        if not img_src:
            raise Exception(f'Failed to get img_src from page {search_url=}')

        return WIKI_URL_BASE + img_src

    def _flush(self):
        with open(self.filename, 'w') as f:
            json.dump(self.cache, f, indent=4, sort_keys=True, separators=(',', ': '))
            f.write('\n')

    @staticmethod
    def _read_cache(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except:
            return {}