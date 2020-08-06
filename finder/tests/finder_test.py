#!/usr/bin/env python3
"""tests for finder.py"""

import os
import random
import re
import string
from subprocess import getstatusoutput

prg = './finder.py'
fox = './tests/fox.txt'
preamble = './tests/preamble.txt'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_no_args():
    """Dies on no arguments"""

    rv, out = getstatusoutput(prg)
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_length():
    """Dies on bad length"""

    bad = random.choice(range(-10, 0))
    rv, out = getstatusoutput(f'{prg} -l {bad} {fox}')
    assert rv != 0
    assert out.lower().startswith('usage')
    assert re.search(f'--len "{bad}" must be > 0', out)


# --------------------------------------------------
def test_bad_file():
    """Dies on bad file"""

    bad = random_string()
    rv, out = getstatusoutput(f'{prg} -l 3 {bad}')
    assert rv != 0
    assert out.lower().startswith('usage')
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_fox_3():
    """test runs ok"""

    assert os.path.isfile(fox)
    rv, out = getstatusoutput(f'{prg} {fox}')
    assert rv == 0
    lines = list(map(str.strip, out.splitlines()))
    assert len(lines) == 4
    assert lines == ['1: The', '2: fox', '3: the', '4: dog']


# --------------------------------------------------
def test_preamble_10():
    """test runs ok"""

    assert os.path.isfile(preamble)
    rv, out = getstatusoutput(f'{prg} --len 10 {preamble}')
    assert rv == 0
    lines = list(map(str.strip, out.splitlines()))
    assert len(lines) == 1
    assert lines == ['1: separation']


# --------------------------------------------------
def test_fox_and_preamble_5():
    """test runs ok"""

    assert os.path.isfile(preamble)
    rv, out = getstatusoutput(f'{prg} --len 10 {preamble} {fox}')
    assert rv == 0
    lines = list(map(str.strip, out.splitlines()))
    assert len(lines) == 1
    assert lines == ['1: separation']


# --------------------------------------------------
def test_dies_none_found():
    """returns error when no words found"""

    rv, out = getstatusoutput(f'{prg} --len 20 {preamble} {fox}')
    assert rv != 0
    assert out == 'Found no words of length 20!'


# --------------------------------------------------
def random_string():
    """generate a random string"""

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
