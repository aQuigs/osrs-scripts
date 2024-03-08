import json

from icon_cache import IconCache


def main(bis_input_filename, output_filename, id_cache_filename):
    with open(bis_input_filename) as f:
        items = [line.rstrip() for line in f]

    id_cache = IconCache(id_cache_filename)
    with open(output_filename, 'w') as f:
        for item_name in items:
            print(f"Processing item: {item_name}")

            img_url = id_cache.get(item_name)
            f.write(f"{item_name},{img_url},false\n")


if __name__ == '__main__':
    main(
        bis_input_filename='data/bis-items.txt',
        output_filename='data/output-bis.csv',
        id_cache_filename='data/item-image-cache.json'
    )
