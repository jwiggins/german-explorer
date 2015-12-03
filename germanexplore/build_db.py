# -*- coding: utf8 -*-
from __future__ import print_function

import argparse
import re
import sqlite3 as sql

# A regex for parsing words and their part of speech annotation
ENTRY_REGEX = re.compile(r'(?P<word>[^\{]+) \{(?P<pos>.+)\}')
DB_INIT_SCRIPT = """
create table germandict(
    german text,
    english text,
    partofspeech text
);

create unique index german_idx on germandict (german);
"""
INSERT_STMT = 'insert into germandict values (?, ?, ?)'


def parse_dict_into_db(src, db):
    """ Parse a dictionary file and add it to a database.
    """
    words = set()
    cur = db.cursor()
    with open(src, 'r') as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            ger, eng, pos = parse_dict_line(line.strip())
            if ger not in words:
                cur.execute(INSERT_STMT, (ger, eng, pos))
                words.add(ger)


def parse_dict_line(line):
    """ Parse a single line from the dictionary file.
    """
    de, en = line.split('::')
    de, en = de.split('|')[0], en.split('|')[0]
    de, en = de.split(';')[0], en.split(';')[0]
    de = de.split('[')[0]
    match = ENTRY_REGEX.match(de)
    if match:
        de, pos = match.group('word'), match.group('pos')
    else:
        de, pos = de.strip(), 'n/a'
    en = en.strip()

    return de, en, pos


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--src', type=str, required=True,
                        help='The DING dictionary file to ingest.')
    parser.add_argument('-d', '--dest', default='dict.db',
                        help='The path to the output database file')
    args = parser.parse_args()

    db = sql.connect(args.dest)
    db.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    with db:
        db.executescript(DB_INIT_SCRIPT)
    try:
        parse_dict_into_db(args.src, db)
    finally:
        db.commit()
        db.close()

if __name__ == '__main__':
    main()
