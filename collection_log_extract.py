import json

from utils import read_cache, write_cache, get_icon_url


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


if __name__ == '__main__':
    main('data/collectionlog-JackRawthorp.json', 'data/output-JackRawthorp.csv', 'data/item-image-cache.json')
