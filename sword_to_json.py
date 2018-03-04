import argparse
import time
from pathlib import Path
from pysword.modules import SwordModules
from py.helpers import does_bible_json_exist
from py.helpers import write_bible_json
from py.Report import Report

# from pprint import pprint  # pprint(vars(book))
default_encoding = 'utf-8'


# noinspection PyProtectedMember
def get_bible_json(path, overwrite):
    # load sword module
    modules = SwordModules(path)
    found_modules = modules.parse_modules()
    keys = found_modules.keys()
    assert len(keys) == 1
    version = list(keys)[0]
    module = found_modules[version]
    report = Report(version)

    print('==================================================')
    print(f'{version} - processing in progress, please wait')

    # get metadata
    language = module['lang']
    meta = {
        'source': 'sword',
        'swordVersion': module['version'],
        'swordVersionDate': module['swordversiondate'],
        'encoding': module['encoding'].lower() if module.get('encoding') else None,
        'language': language,
        'license': module['distributionlicense']
    }

    actual_encoding = meta['encoding']
    assert actual_encoding == default_encoding or actual_encoding is None, f'{version} - expected module encoding {default_encoding} but got {actual_encoding}'

    # skip if JSON exists
    exists_obj = does_bible_json_exist(version, language)
    if exists_obj['exists'] and not overwrite:
        print(f'{version} - skipping, already exists')
        return None

    # get raw bible books
    # noinspection PyBroadException
    try:
        bible = modules.get_bible_from_module(version)
    except Exception as e:
        print(f'{version} - aborting, pysword failure .. {e}')
        return None

    assert bible._encoding == default_encoding or bible._encoding is None, f'{version} - expected bible encoding {default_encoding} but got {bible._encoding}'
    bible_structure = bible.get_structure()
    assert bible_structure._book_offsets is None

    if bible_structure._books.get('ot') is None:
        print(f'{version} - aborting, old testament missing')
        return None

    if bible_structure._books.get('nt') is None:
        print(f'{version} - aborting, new testament missing')
        return None

    raw_books = bible_structure._books['ot'] + bible_structure._books['nt']
    assert len(raw_books) == 66

    # init processing
    start = time.time()
    chapter_count = 0
    verse_count = 0

    # main processing
    books = []
    for book_idx, book in enumerate(raw_books):

        report.processed(book_idx + 1, book.osis_name, start)
        range_chapters = range(0, book.num_chapters)

        chapters = []
        for chapter_idx in range_chapters:

            chapter_num = chapter_idx + 1
            raw_verses = book.get_indicies(chapter_num)

            verses = []
            for verse_idx, xxxxx in enumerate(raw_verses):

                verse_num = verse_idx + 1

                try:
                    text = bible.get(books=[book.name], chapters=[chapter_num], verses=[verse_num])
                except Exception as e:
                    if 'incorrect header' in str(e):
                        text = None
                    else:
                        raise e

                if text is not None:
                    # TIDYUP - trim
                    text = text.strip()

                if text == '':
                    text = None

                if text is not None:

                    # TIDYUP - remove double spaces
                    while '  ' in text:
                        text = text.replace('  ', ' ')

                    # TIDYUP - replace horrible chars
                    text = text.replace('\u2013', '-')
                    text = text.replace('\u2019', '\'')

                verses.append({
                    'number': verse_num,
                    'text': text
                })
                verse_count += 1

            chapters.append({
                'number': chapter_num,
                'verses': verses
            })
            chapter_count += 1

        books.append({
            'name': book.osis_name,
            'verses_per_chapter': book.chapter_lengths,
            'chapters': chapters,
        })

    print()
    report.summary(len(books), chapter_count, verse_count)
    assert chapter_count == 1189
    return {
        'version': version,
        'meta': meta,
        'books': books
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--partials', action='store_true')
    args = parser.parse_args()
    overwrite = args.overwrite
    partials = args.partials

    paths = Path('sword-modules').glob('**/*.zip')
    for path in paths:
        bible = get_bible_json(str(path), overwrite)
        if bible is not None:
            write_bible_json(bible, partials)


if __name__ == '__main__':
    main()
