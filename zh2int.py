#!/usr/bin/python3
# 把表格當中的地支轉成整數， 子=>1、丑=>2、..亥=>0

import sys

earth = '亥子丑寅卯辰巳午未申酉戌'
for line in sys.stdin:
    out = []
    for x in line.rstrip().split(','):
        n = earth.find(x)
        out.append(str(n) if n>=0 else x)
    print(','.join(out))
