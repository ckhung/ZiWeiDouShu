#!/usr/bin/python3
# 把表格當中的地支轉成整數， 子=>1、丑=>2、..亥=>0

import sys

earth = { x:str(i) for (i,x) in enumerate('亥子丑寅卯辰巳午未申酉戌') }
for line in sys.stdin:
    out = [earth.get(x, x) for x in line.rstrip().split(',')]
    print(','.join(out))
