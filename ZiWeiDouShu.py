#!/usr/bin/python3
# 參考資料:
# "紫微精解" 天滴子著 希代出版
# "紫微斗數新詮" 慧心齋主著 時報出版

import sys, re

heaven = [ '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬' ]
earth = [ '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌' ]
house = [ '命宮', '兄弟', '夫妻', '子女', '財帛', '疾厄', '遷移', '僕役', '官祿', '田宅', '福德', '父母' ]

def vert_print(out, r, c, string):
    # 將字串轉為單個中文字元列表（Perl 原用 regex (...)g）
    s = list(string)
    for i in range(len(s)):
        if r + i < len(out):
            out[r + i][c] = s[i]

def num2full(n):
    FN = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
    r = ''
    # 模仿 do-while 邏輯
    temp_n = n
    while True:
        r = FN[temp_n % 10] + r
        temp_n = int(temp_n / 10)
        if temp_n <= 0:
            break
    return r

def display_chart(chart):
    person = chart['person']
    wd, ht = 9, 9
    pos = [
        [ 3, 3 ], [ 3, 2 ], [ 3, 1 ], [ 3, 0 ], [ 2, 0 ], [ 1, 0 ], 
        [ 0, 0 ], [ 0, 1 ], [ 0, 2 ], [ 0, 3 ], [ 1, 3 ], [ 2, 3 ]
    ]

    # 畫一張空白命盤
    out = [["  " for _ in range(wd * 4 + 1)] for _ in range(ht * 4 + 1)]
    
    for i in range(5):
        # 橫線
        for j in range(wd * 4 + 1):
            out[i * ht][j] = "--"
        # 縱線
        for row in range(ht * 4 + 1):
            out[row][i * wd] = " |"

    for i in range(5):
        for j in range(5):
            out[i * ht][j * wd] = " +"

    # 打通中間空格
    for r in range(ht + 1, ht * 3):
        for c in range(wd + 1, wd * 3):
            out[r][c] = "  "
    for r in range(ht + 1, ht * 3):
        out[r][2 * wd] = "  "

    # 填入資料
    birth_info = f"{heaven[person['heaven']]}{earth[person['earth']]}年{num2full(person['month'] if person['month'] > 0 else 12)}月{num2full(person['day'])}日{earth[person['hour']]}時生"
    vert_print(out, ht + 3, int(wd * 3 - 1), birth_info)
    vert_print(out, ht * 2 + 3, int(wd * 1.5), f"{chart['element']}局")

    for e in range(12):
        r, c = pos[e][0] * ht, pos[e][1] * wd
        vert_print(out, r + ht - 2, c + wd - 1, heaven[chart[e]['heaven']] + earth[e])
        vert_print(out, r + ht - 2, c + int(wd / 2) + 1, house[chart[e]['house']])
        if chart['body'] == e:
            vert_print(out, r + ht - 2, c + int(wd / 2), '身宮')
        
        if 'star' in chart[e]:
            for i in range(len(chart[e]['star'])):
                s = chart[e]['star'][i]
                # 去除前綴數字與空格 (s =~ s/^[\w\s]*//)
                s = re.sub(r'^\d\s+', '', s)
                vert_print(out, r + 1, c + wd - i - 1, s)

    for i in range(ht * 4 + 1):
        print("".join(out[i]))
    print('')

def list_chart(chart):
    person = chart['person']
    print(f"{heaven[person['heaven']]}{earth[person['earth']]}年{person['month']}月{person['day']}日{earth[person['hour']]}時生 {chart['element']}局")
    print(f"命宮 {earth[chart['fate']]} / 身宮 {earth[chart['body']]}")
    for i in range(12):
        stars = " ".join(chart[i].get('star', []))
        import re
        stars = re.sub(r'\d ', '', stars)
        print(f"{house[chart[i]['house']]} {earth[i]}: {stars}")

def create_chart(person):
    chart = {} # 命盤, 以地支為註標
    chart['person'] = person
    for i in range(12):
        chart[i] = {'star': []}

    # 起寅首
    head = ((person['heaven'] % 5) * 2 + 1) % 10
    for e in range(12):
        chart[(e + 3) % 12]['heaven'] = (e + head) % 10

    # 起命身宮
    chart['body'] = (person['month'] + person['hour'] + 1) % 12
    chart['fate'] = (person['month'] - person['hour'] + 15) % 12

    # 排列十二宮位
    for e in range(12):
        chart[(chart['fate'] - e + 12) % 12]['house'] = e

    # 定五行局
    # 再次驗證： https://www.ai5429.com/c/505.htm
    tab = [
        [4,3,5,6,2], [2,4,3,5,6], [5,6,2,4,3],
        [6,2,4,3,5], [3,5,6,2,4], [2,4,3,5,6]
    ]
    t = tab[int((chart['fate'] - 1) / 2)][4 - (person['heaven'] + 4) % 5]
    chart['element'] = ['', '', '水二', '木三', '金四', '土五', '火六'][t]

    # 四化表
    m = [
        [ "破軍", "巨門", "太陰", "貪狼" ],
        [ "廉貞", "破軍", "武曲", "太陽" ],
        [ "天機", "天梁", "紫微", "太陰" ],
        [ "天同", "天機", "文昌", "廉貞" ],
        [ "太陰", "天同", "天機", "巨門" ],
        [ "貪狼", "太陰", "右弼", "天機" ],
        [ "武曲", "貪狼", "天梁", "文曲" ],
        [ "太陽", "武曲", "天同", "太陰" ],
        [ "巨門", "太陽", "文曲", "文昌" ],
        [ "天梁", "紫微", "左輔", "武曲" ]
    ]
    
    morph = {}
    morph_tags = ['祿', '權', '科', '忌']
    for idx, star_name in enumerate(m[person['heaven']]):
        morph[f"1 {star_name}"] = morph_tags[idx]

    # 起紫微
    ms = (6 - person['day']) % t
    ms = [3, 2, 5, 0, 7, -2][ms]
    ms = int((person['day'] - 1) / t + ms + 12) % 12
    chart[ms]['star'].append('1 紫微')

    # 安甲級十四顆正星
    main_star = {
        '1 天機': {'cw': 1, 'ofs': -1},
        '1 太陽': {'cw': 1, 'ofs': -3},
        '1 武曲': {'cw': 1, 'ofs': -4},
        '1 天同': {'cw': 1, 'ofs': -5},
        '1 廉貞': {'cw': 1, 'ofs': 4},
        '1 天府': {'cw': -1, 'ofs': 6},
        '1 太陰': {'cw': -1, 'ofs': 7},
        '1 貪狼': {'cw': -1, 'ofs': 8},
        '1 巨門': {'cw': -1, 'ofs': 9},
        '1 天相': {'cw': -1, 'ofs': 10},
        '1 天梁': {'cw': -1, 'ofs': 11},
        '1 七殺': {'cw': -1, 'ofs': 12},
        '1 破軍': {'cw': -1, 'ofs': 4},
    }

    for key, val in main_star.items():
        st = f"{key}化{morph[key]}" if key in morph else key
        chart[(val['cw'] * ms + val['ofs'] + 12) % 12]['star'].append(st)

    # 安干系諸星
    heaven_star = {
        '1 祿存': [ 1, 3, 4, 6, 7, 6, 7, 9, 10, 0 ],
        '1 擎羊': [ 2, 4, 5, 7, 8, 7, 8, 10, 11, 1 ],
        '1 陀羅': [ 0, 2, 3, 5, 6, 5, 6, 8, 9, 11 ],
        '1 天魁': [ 4, 2, 1, 0, 0, 2, 1, 2, 7, 4 ],
        '1 天越': [ 6, 8, 9, 10, 10, 8, 9, 8, 3, 6 ],
        '4 天官': [ 7, 8, 5, 6, 3, 4, 10, 0, 10, 11 ],
        '4 天福': [ 6, 10, 9, 1, 0, 4, 3, 7, 6, 7 ],
        '3 天廚': [ 0, 6, 7, 1, 6, 7, 9, 3, 7, 10 ],
    }
    for key, val in heaven_star.items():
        chart[val[person['heaven']]]['star'].append(key)

    # 安月系諸星
    chart[(person['month'] + 4) % 12]['star'].append('1 左輔')
    chart[(12 - person['month']) % 12]['star'].append('1 右弼')
    chart[(person['month'] + 9) % 12]['star'].append('2 天刑')
    chart[(person['month'] + 1) % 12]['star'].append('2 天姚')

    chart[[7, 9, 11, 1, 3, 5, 7][int((person['month'] + 1) / 2)]]['star'].append('3 解神')
    chart[[3, 6, 9, 0][person['month'] % 4]]['star'].append('3 天巫')
    chart[[3, 11, 6, 5, 3, 8, 4, 0, 8, 3, 7, 11][person['month']]]['star'].append('3 天月')
    chart[[3, 1, 11, 9, 7, 5][person['month'] % 6]]['star'].append('3 陰煞')

    # 安時系諸星
    hour_star = {
        '1 文昌': {'cw': -1, 'ofs': 0},
        '1 文曲': {'cw': 1, 'ofs': 4},
        '1 地劫': {'cw': 1, 'ofs': -1},
        '1 空劫': {'cw': -1, 'ofs': 1},
        '3 臺輔': {'cw': 1, 'ofs': 6},
        '3 封誥': {'cw': 1, 'ofs': 2},
    }
    for key, val in hour_star.items():
        st = f"{key}化{morph[key]}" if key in morph else key
        chart[(val['cw'] * person['hour'] + val['ofs'] + 12) % 12]['star'].append(st)

    chart[(person['hour'] + [9, 2, 3, 1][person['earth'] % 4]) % 12]['star'].append('1 火星')
    chart[(person['hour'] + [10, 10, 10, 3][person['earth'] % 4]) % 12]['star'].append('1 鈴星')

    # 安支系諸星
    earth_star = {
        '3 天空': {'cw': 1, 'ofs': 1},
        '3 天哭': {'cw': -1, 'ofs': 8},
        '3 天虛': {'cw': 1, 'ofs': 6},
        '3 龍池': {'cw': 1, 'ofs': 4},
        '3 鳳閣': {'cw': -1, 'ofs': 12},
        '3 紅鸞': {'cw': -1, 'ofs': 5},
        '3 天喜': {'cw': -1, 'ofs': 11},
        '3 天德': {'cw': 1, 'ofs': 9},
        '3 月德': {'cw': 1, 'ofs': 5},
    }
    for key, val in earth_star.items():
        chart[(val['cw'] * person['earth'] + val['ofs'] + 12) % 12]['star'].append(key)

    chart[(18 - person['earth'] % 4 * 3) % 12]['star'].append('1 天馬')
    chart[(int(person['earth'] / 3) * 3 + 3) % 12]['star'].append('3 孤辰')
    chart[(int(person['earth'] / 3) * 3 + 11) % 12]['star'].append('3 寡宿')
    chart[[2, 9, 10, 11, 6, 7, 8, 3, 4, 5, 0, 1][person['earth']]]['star'].append('3 蜚廉')
    chart[(22 - person['earth'] % 3 * 4) % 12]['star'].append('3 破碎')
    chart[(20 - person['earth'] % 4 * 3) % 12]['star'].append('3 華蓋')
    chart[(13 - person['earth'] % 4 * 3) % 12]['star'].append('3 咸池')
    chart[(chart['fate'] + person['earth'] + 11) % 12]['star'].append('3 天才')
    chart[(chart['body'] + person['earth'] + 11) % 12]['star'].append('3 天壽')

    # Gemini 補充4級星：
    chart[(person['earth'] + 9) % 12]['star'].append('4 年解')

    # 各宮按星等排序
    for e in range(12):
        chart[e]['star'].sort()

    return chart

# 主程式邏輯
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("使用範例: 以農曆生辰為甲寅年5月7日申時為例, 請下", file=sys.stderr)
        print("python fortune.py 1 3 5 7 9", file=sys.stderr)
        sys.exit(1)

    try:
        args = [int(x) for x in sys.argv[1:]]
    except ValueError:
        print("錯誤: 參數必須為數字", file=sys.stderr)
        sys.exit(1)

    person = {
        'heaven': args[0] % 10,
        'earth': args[1] % 12,
        'month': args[2] % 12,
        'day': args[3],
        'hour': args[4] % 12,
    }

    chart = create_chart(person)
    display_chart(chart)
    list_chart(chart)
