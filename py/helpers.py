import json
import os
import re


def does_bible_json_exist(version):
    path = os.path.abspath(f'bibles/{version}')
    filename = f'{path}/{version}.json'
    return {
        'exists': os.path.exists(filename),
        'path': path,
        'filename': filename
    }


def write_bible_json(bible, partials, encoding):
    version = bible['version']
    exists_obj = does_bible_json_exist(version)

    if not os.path.exists(exists_obj['path']):
        os.makedirs(exists_obj['path'])

    print(f'{version} - writing JSON file')
    with open(exists_obj['filename'], 'w', encoding=encoding) as f:
        json.dump(bible, f, ensure_ascii=False)

    if partials:
        for book in bible['books']:
            is_genesis = book['name'].lower().startswith('ge') or book['name'].lower().startswith('gn')
            if is_genesis:
                book['verses_per_chapter'] = book['verses_per_chapter'][:3]
            else:
                book['verses_per_chapter'] = []

            for chapter in book['chapters']:
                if is_genesis and chapter['number'] == 1:
                    chapter['verses'] = chapter['verses'][:3]
                else:
                    chapter['verses'] = []

        partial_filename = re.sub('.json$', '-partial.json', exists_obj['filename'])
        with open(partial_filename, 'w', encoding=encoding) as f:
            f.write(json.dumps(bible, indent=2, ensure_ascii=False))
