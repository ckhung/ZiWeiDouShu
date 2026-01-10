#!/usr/bin/python3

import argparse, sys, random, subprocess

parser = argparse.ArgumentParser(description='比對 Perl 與 Python 版本的紫微斗數輸出')
parser.add_argument('-n', type=int, default=30, help='測試幾組資料')
args_parsed = parser.parse_args()

for i in range(args_parsed.n):
    # 產生隨機生辰參數
    # 年干(0-9), 年支(0-11), 月(0-11), 日(1-28), 時(0-11)
    rand_args = [
        random.randint(0, 9),
        random.randint(0, 11),
        random.randint(0, 11),
        random.randint(1, 28),
        random.randint(0, 11)
    ]
    
    str_args = [str(x) for x in rand_args]
    print(' '.join(str_args))

    with open('/tmp/pl.txt', 'w') as f_pl:
        subprocess.run(['perl', 'ZiWeiDouShu.pl'] + str_args, stdout=f_pl)
    with open('/tmp/py.txt', 'w') as f_py:
        subprocess.run(['python3', 'ZiWeiDouShu.py'] + str_args, stdout=f_py)
    result = subprocess.run(['diff', '/tmp/pl.txt', '/tmp/py.txt'], capture_output=True, text=True)

