#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-08-06
Purpose: Find words in a file of given length
"""

import argparse
import re
import sys
from itertools import starmap
from functools import partial
from typing import TextIO, NamedTuple, List


class Args(NamedTuple):
    file: List[TextIO]
    length: int


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Find words in a file of given length',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input file(s)',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-l',
                        '--len',
                        help='Length of words to find',
                        metavar='int',
                        type=int,
                        default=3)

    args = parser.parse_args()

    if args.len < 0:
        parser.error(f'--len "{args.len}" must be > 0')

    return Args(args.file, args.len)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    if words := find_words(args.length, args.file):
        print('\n'.join(
            starmap(lambda i, w: f'{i:3}: {w}', enumerate(words, 1))))
    else:
        sys.exit(f'Found no words of length {args.length}!')


# --------------------------------------------------
def find_words(word_length: int, fhs: List[TextIO]) -> List[str]:
    """Find words in a given text of a certain length"""

    words: List[str] = []
    clean = partial(re.sub, '[^a-zA-Z]', '')
    accept = lambda word: len(word) == word_length

    for fh in fhs:
        for line in fh:
            words.extend(filter(accept, map(clean, line.split())))

    return words


# --------------------------------------------------
if __name__ == '__main__':
    main()
