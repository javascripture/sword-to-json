import math
import sys
import time


class Report:

    expected_book_count = 66

    def __init__(self, version):
        self.version = version

    def processed(self, book_idx, book_name, start):
        elapsed = str(math.floor(time.time() - start)).zfill(3)
        str_book_idx = str(book_idx).zfill(2)
        str_book_name = book_name.ljust(6)
        bar = '|' + '#' * (book_idx - 1) + ' ' * (Report.expected_book_count - book_idx) + '|'
        msg = f'{self.version} - {str_book_idx} {str_book_name} {bar} {elapsed} sec'
        sys.stdout.write('\r' + msg)
        sys.stdout.flush()

    def summary(self, books, chapters, verses):
        print(f'{self.version} - processing complete with {books} books {chapters} chapters {verses} verses')
