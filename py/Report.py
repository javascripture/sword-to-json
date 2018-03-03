import math
import sys
import time


class Report:

    def __init__(self, version):
        self.version = version

    def processed(self, book_num, book_name, start):
        str_book_num = str(book_num).zfill(2)
        str_book_name = book_name.ljust(6)
        bar = '|' + '#' * (book_num - 1) + ' ' * (66 - book_num) + '|'
        elapsed = str(math.floor(time.time() - start)).zfill(3)
        msg = f'{self.version} - {str_book_num} {str_book_name} {bar} {elapsed} sec'
        sys.stdout.write('\r' + msg)
        sys.stdout.flush()

    def summary(self, books, chapters, verses):
        print(f'{self.version} - processing complete with {books} books {chapters} chapters {verses} verses')
