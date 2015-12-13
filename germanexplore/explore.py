# -*- coding: utf8 -*-
from __future__ import print_function

import argparse
import sqlite3 as sql

FIND_STMT = "SELECT * FROM germandict WHERE german=?"
ENTRY_TMPL = u"""\
{0} - [{2}]:
{1}\
"""
VERB_PREFIXES = (
'ab', 'an', 'auf', 'aus', 'be', 'bei', 'da', 'dabei', 'dar', 'daran',
'dazwischen', 'durch', 'ein', 'emp', 'ent', 'er', 'fehl', 'fern', 'fest',
'fort', 'frei', 'gegenüber', 'gleich', 'heim', 'her', 'herab', 'heran',
'herauf', 'heraus', 'herbei', 'herein', 'herüber', 'herum', 'herunter',
'hervor', 'hin', 'hinab', 'hinauf', 'hinaus', 'hinein', 'hinter', 'hinterher',
'hinunter', 'hinweg', 'hinzu', 'hoch', 'los', 'miss', 'mit', 'nach',
'nebenher', 'nieder', 'statt', 'über', 'um', 'unter', 'ver', 'voll', 'vor',
'voran', 'voraus', 'vorbei', 'vorüber', 'vorweg', 'weg', 'weiter', 'wider',
'wieder', 'zer', 'zu', 'zurecht', 'zurück', 'zusammen',
)


def list_related_verbs(cursor, word):
    """Find all the prefixed forms of a verb.
    """
    for pref in VERB_PREFIXES:
        for row in cursor.execute(FIND_STMT, (pref+word,)):
            print(ENTRY_TMPL.format(*row))

def lookup_words(db):
    """ Look words up in the dictionary database file.
    """
    cursor = db.cursor()
    while True:
        print("Enter a German word to look up: ", end='')
        try:
            word = raw_input()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        for row in cursor.execute(FIND_STMT, (word,)):
            print(ENTRY_TMPL.format(*row))
            if row[2] == 'vi':
                list_related_verbs(cursor, word)
            break
        else:
            print("Not found")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--dictionary', default='dict.db',
                        help='The path to the dictionary database file')
    args = parser.parse_args()

    db = sql.connect(args.dictionary)
    db.text_factory = lambda x: unicode(x, "utf-8", "ignore")
    try:
        lookup_words(db)
    finally:
        db.close()

if __name__ == '__main__':
    main()
