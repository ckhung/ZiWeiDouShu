#!/usr/bin/python3

import argparse, sys, random, subprocess

parser = argparse.ArgumentParser(description='比對 py 版紫微斗數輸出與其他語言版本是否一致')
parser.add_argument('-n', type=int, default=30, help='測試幾組資料')
parser.add_argument('-l', '--lang', type=str, default='js', help='跟哪個語言的版本比較 (js 或 pl)')
args = parser.parse_args()

if args.lang == 'js':
    print(f'用亂數產生 {args.n} 筆生辰， 比對 python 版 vs javascript 版...')
elif args.lang == 'pl':
    print(f'用亂數產生 {args.n} 筆生辰， 比對 python 版 vs perl 版...')
else:
    parser.print_help(sys.stderr)
    sys.exit(1)

for i in range(args.n):
    # 產生隨機生辰參數
    # 年干(0-9), 年支(0-11), 月(0-11), 日(1-28), 時(0-11)
    rand_args = [
        random.randint(0, 9),
        random.randint(0, 11),
        random.randint(0, 11),
        random.randint(1, 29),
        random.randint(0, 11)
    ]
    
    str_args = [str(x) for x in rand_args]
    print(' '.join(str_args))

    if args.lang == 'pl':
        with open('/tmp/py.txt', 'w') as f_py:
            subprocess.run(['python3', 'ZiWeiDouShu.py'] + str_args, stdout=f_py)
        with open('/tmp/other.txt', 'w') as f_other:
            subprocess.run(['perl', 'ZiWeiDouShu.pl'] + str_args, stdout=f_other)
    else:
        with open('/tmp/py.txt', 'w') as f_py:
            subprocess.run(['python3', 'ZiWeiDouShu.py', '-o', 'list'] + str_args, stdout=f_py)
        with open('/tmp/other.txt', 'w') as f_other:
            subprocess.run(['nodejs', 'ZiWeiDouShu.js'] + str_args, stdout=f_other)
    result = subprocess.run(['diff', '/tmp/py.txt', '/tmp/other.txt'], capture_output=True, text=True)
    if result.stdout != '':
        print(result.stdout)


# 有疑義時可查詢： 紫微斗數命盤： https://fate.windada.com/cgi-bin/fate
# 9 5 11 22 2 <= 四化少兩化 已更正

