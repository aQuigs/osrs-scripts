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


def main(log_input_filename, output_filename, id_cache_filename):
    with open(log_input_filename) as f:
        data = json.load(f)

    id_cache = read_cache(id_cache_filename)
    seen_item_ids = set()

    with open(output_filename, 'w') as f:
        for tab in data['tabs'].keys():
            tab_data = data['tabs'][tab]
            for boss in tab_data.keys():
                print('-'*50)
                print(f"Processing boss: {boss}")
                print('-'*50)

                boss_log = tab_data[boss]['items']
                for item_data in boss_log:
                    img_url = get_icon_url(id_cache, item_data['name'], str(item_data['id']))
                    f.write(
                        f"{item_data['name']},"
                        f"{tab},"
                        f"{boss},"
                        f'=IMAGE("{img_url}"),'
                        f"{item_data['obtained']},"
                        f"{item_data.get('quantity', '')},"
                        f"{'(Rare)' in boss},"
                        f"{item_data['id'] in seen_item_ids}\n"
                    )
                    seen_item_ids.add(item_data['id'])

                write_cache(id_cache, id_cache_filename)


def get_icon_url(cache, name, id):
    if id not in cache:
        cache[id] = find_url(name, id)

    return cache[id]


def find_url(name, id):
        icon_id = ICON_OVERRIDES.get(id, id)
        
        print(f"Finding icon for {name=} {id=} {icon_id=}..")
        
        wiki_page = urlopen(Request(
            f"{WIKI_URL_BASE}{LOOKUP_SUFFIX}?type=item&id={icon_id}&name={url_encode(name)}",
            headers={'User-Agent' : "Magic Browser"}
        )).read()
        
        pq = PyQuery(wiki_page)
        img_src = pq('.inventory-image>a:last-child>img').attr('src')
        
        url = WIKI_URL_BASE + img_src


def write_cache(cache, filename):
    with open(filename, 'w') as f:
        json.dump(cache, f)


def read_cache(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        return {}


if __name__ == '__main__':
    main('data/collectionlog-JackRawthorp.json', 'data/output-JackRawthorp.csv', 'data/item-image-cache.json')
