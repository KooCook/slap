#!/usr/bin/env python
import sys
import re

from functools import reduce


def ticks_to_brackets(line: str, m: re.Match) -> str:
    first, *mid, last = s = m.group(0)
    assert first == '`' == last, m
    return line.replace(s, f'[{"".join(mid)}]')


def escape_slash_to_double(m: re.Match) -> str:
    return m.group(0).replace(r"\'", "''")


if __name__ == '__main__':
    # py change_sql_dialect.py infile outfile
    infile = sys.argv[1]
    outfile = sys.argv[2]
    with open(infile, 'r', encoding='utf-8') as file:
        contents = file.read()
    lines = contents.splitlines(keepends=True)
    lst = []
    for i, line in enumerate(lines):
        if line.startswith('INSERT INTO '):
            # Replace all occurrence of `pattern` using function (first arg)
            changed = reduce(ticks_to_brackets, re.finditer(r"`.+?`", line), line)
        else:
            changed = re.sub(r"'([^']*?(\\')[^']*?)*'", escape_slash_to_double, line)
        lst.append(changed)
        # if 100 < i < 120:
        #     print(i, ':', changed)
    with open(outfile, 'w', encoding='utf-8') as file:
        file.write(''.join(lst))
    print("Don't forget to manually change "
          "'START TRANSACTION;' to 'BEGIN TRANSACTION' "
          "and optionally add 'PRAGMA foreign_keys=OFF;' "
          "and comment out the SETs")
