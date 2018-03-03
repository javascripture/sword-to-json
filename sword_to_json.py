from pathlib import Path
import argparse
import time
from pysword.modules import SwordModules
from py.helpers import does_bible_json_exist
from py.helpers import write_bible_json
from py.Report import Report
from pprint import pprint  # pprint(vars(book))


# noinspection PyProtectedMember
def get_bible_json(path, overwrite):
    expected_encoding = 'utf-8'

    modules = SwordModules(path)
    found_modules = modules.parse_modules()
    # pprint(found_modules)
    keys = found_modules.keys()
    assert (len(keys) == 1)
    version = list(keys)[0]
    module = found_modules[version]

    meta = {
        'source': 'sword',
        'swordVersion': module['version'],
        'swordVersionDate': module['swordversiondate'],
        'encoding': module['encoding'].lower(),
        'language': module['lang'],
        'license': module['distributionlicense']
    }
    assert (meta['encoding'] == expected_encoding)

    report = Report(version)

    exists_obj = does_bible_json_exist(version)
    if exists_obj['exists'] and not overwrite:
        print(f'{version} - skipping')
        return None

    bible = modules.get_bible_from_module(version)
    # pprint(vars(bible))

    assert (bible._encoding == expected_encoding)

    bible_structure = bible.get_structure()
    # pprint(vars(bible_structure))

    assert (bible_structure._book_offsets is None)
    raw_books = bible_structure._books['ot'] + bible_structure._books['nt']

    print('==================================================')
    print(f'{version} - processing in progress, please wait')

    all_verses = []
    books = []

    start = time.time()

    for book_idx, book in enumerate(raw_books):

        pprint(vars(book))

        report.processed(book_idx + 1, book.osis_name, start)

        range_chapters = range(1, book.num_chapters + 1)
        chapters = []

        for chapter in range_chapters:

            raw_verses = book.get_indicies(chapter)
            verses = []

            for verseIdx, verse in enumerate(raw_verses):

                # verse_ref = book.osis_name + ' ' + str(chapter) + ':' + str(verseIdx + 1)

                try:
                    text = bible.get(books=[book.name], chapters=[chapter], verses=[verseIdx + 1])
                except Exception as e:
                    if 'incorrect header' in str(e):
                        text = None
                    else:
                        raise e

                if text is not None:
                    text = text.strip()

                if text == '':
                    text = None

                if text is not None:
                    verse = {
                        'number': verseIdx + 1,
                        'text': text
                    }
                    verses.append(verse)
                    all_verses.append(verse)

            chapters.append({
                'number': chapter,
                'verses': verses
            })

        books.append({
            'name': book.osis_name,
            'chapters': chapters
        })

    print()
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