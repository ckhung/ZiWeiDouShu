#!/usr/bin/perl -w
# 參考資料:
# "紫微精解" 天滴子著 希代出版
# "紫微斗數新詮" 慧心齋主著 時報出版

# use Data::Dumper;

$heaven = [ '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬' ];
$earth = [ '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌' ];
$house = [ '命宮', '兄弟', '夫妻', '子女', '財帛', '疾厄', '遷移', '僕役', '官祿', '田宅', '福德', '父母' ];

sub vert_print {
    my ($out, $r, $c, $str) = @_;
    my (@s) = $str =~ /(...)/g;
    my ($i);
    for ($i=0; $i<=$#s; ++$i) {
	$out->[$r+$i][$c] = $s[$i];
    }
}

sub num2full {
    my ($n) = @_;
    my (@FN) = qw(０ １ ２ ３ ４ ５ ６ ７ ８ ９);
    my ($r) = '';
    do {
	$r = $FN[$n % 10] . $r;
	$n = int($n/10);
    } while ($n>0);
    return $r;
}

sub display_chart {
    my ($chart) = @_;
    my ($person) = $chart->{person};
    my ($out, $e, $i, $j);
    my ($wd, $ht) = (9, 9);
    my ($pos) = [
	[ 3, 3 ], [ 3, 2 ], [ 3, 1 ], [ 3, 0 ], [ 2, 0 ], [ 1, 0 ], 
	[ 0, 0 ], [ 0, 1 ], [ 0, 2 ], [ 0, 3 ], [ 1, 3 ], [ 2, 3 ], 
    ];

    # 畫一張空白命盤
    for ($i=1; $i<$ht*4; ++$i) {
	@{ $out->[$i] } = ("  ") x ($wd*4+1);
    }
    for ($i=0; $i<=4; ++$i) {
	@{ $out->[$i*$ht] } = ("--") x ($wd*4+1);
	map { $_->[$i*$wd] = " |"; } @$out;
    }
    for ($i=0; $i<=4; ++$i) {
	for ($j=0; $j<=4; ++$j) {
	    $out->[$i*$ht][$j*$wd] = " +";
	}
    }
    @{ $out->[2*$ht] }[$wd+1..$wd*3-1] = ("  ") x ($wd*2-1);
    map { $_->[2*$wd] = "  "; } @{$out}[$ht+1..$ht*3-1];

    # 填入資料
    vert_print($out, $ht+3, int($wd*3-1),
	sprintf("%s%s年%s月%s日%s時生",
	    $heaven->[$person->{heaven}], $earth->[$person->{earth}],
	    num2full($person->{month}>0?$person->{month}:12),
	    num2full($person->{day}), $earth->[$person->{hour}]
	)
    );
    vert_print($out, $ht*2+3, int($wd*1.5), "$chart->{element}局");
    for ($e=0; $e<12; ++$e) {
	my ($r, $c) = ($pos->[$e][0]*$ht, $pos->[$e][1]*$wd);
	vert_print($out, $r+$ht-2, $c+$wd-1,
	    $heaven->[$chart->{$e}{heaven}] . $earth->[$e] );
	vert_print($out, $r+$ht-2, $c+int($wd/2)+1,
	    $house->[$chart->{$e}{house}] );
	vert_print($out, $r+$ht-2, $c+int($wd/2), '身宮') if ($chart->{body} == $e);
	for ($i=0; $i<=$#{ $chart->{$e}{star} }; ++$i) {
	    $s = $chart->{$e}{star}[$i];
	    $s =~ s/^[\w\s]*//;
	    vert_print($out, $r+1, $c+$wd-$i-1, $s);
	}
    }
    for ($i=0; $i<=$ht*4; ++$i) {
	print join("", @{$out->[$i]}), "\n";
    }
    print "\n";
}

sub list_chart {
    my ($chart) = @_;
    my ($person) = $chart->{person};
    printf("$heaven->[$person->{heaven}]$earth->[$person->{earth}]年%d月%d日%s時生 $chart->{element}局\n", $person->{month}, $person->{day}, $earth->[$person->{hour}]);
    printf("命宮 $earth->[$chart->{fate}] / 身宮 $earth->[$chart->{body}]\n");
    for ($i=0; $i<12; ++$i) {
	$stars = "@{$chart->{$i}{star}}";
	$stars =~ s/\d //g;
	print("$house->[$chart->{$i}{house}] $earth->[$i]: $stars\n");
    }
}

sub create_chart {
    my ($person) = @_;
    my ($chart);				# 命盤, 以地支為註標
    my ($e);

    $chart->{person} = $person;
    # 起寅首
    $head = (($person->{heaven} % 5) * 2 + 1) % 10;
    for ($e=0; $e<12; ++$e) {
	$chart->{($e+3)%12}{heaven} = ($e + $head) % 10;
    }
    # 起命身宮
    $chart->{body} = ($person->{month} + $person->{hour} + 1) % 12;
    $chart->{fate} = ($person->{month} - $person->{hour} + 15) % 12;
    # 排列十二宮位
    for ($e=0; $e<12; ++$e) {
	$chart->{($chart->{fate}-$e+12)%12}{house} = $e;
    }
    # 定五行局
    # 再次驗證： https://www.ai5429.com/c/505.htm
    my ($tab) = [
	[4,3,5,6,2], [2,4,3,5,6], [5,6,2,4,3],
	[6,2,4,3,5], [3,5,6,2,4], [2,4,3,5,6]
    ];
    my ($t) = $tab->[int(($chart->{fate}-1)/2)][4-($person->{heaven}+4)%5];
    $chart->{element} = ('','','水二','木三','金四','土五','火六')[$t];
    # 四化表
    my ($m) = [
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
    ];
    my (%morph);
    @morph{ map { "1 $_" } @{ $m->[$person->{heaven}] } } = ('祿', '權', '科', '忌');
    # 起紫微
    my ($ms); # main star
    $ms = (6 - $person->{day}) % $t;
    $ms = (3,2,5,0,7,-2)[$ms];
    $ms = int(($person->{day}-1)/$t + $ms + 12) % 12;
    push @{ $chart->{$ms}{star} }, '1 紫微';
    # 安甲級十四顆正星
    my ($main_star) = {
	'1 天機' => { cw=> 1, ofs=>-1 },
	'1 太陽' => { cw=> 1, ofs=>-3 },
	'1 武曲' => { cw=> 1, ofs=>-4 },
	'1 天同' => { cw=> 1, ofs=>-5 },
	'1 廉貞' => { cw=> 1, ofs=> 4 },
	'1 天府' => { cw=>-1, ofs=> 6 },
	'1 太陰' => { cw=>-1, ofs=> 7 },
	'1 貪狼' => { cw=>-1, ofs=> 8 },
	'1 巨門' => { cw=>-1, ofs=> 9 },
	'1 天相' => { cw=>-1, ofs=>10 },
	'1 天梁' => { cw=>-1, ofs=>11 },
	'1 七殺' => { cw=>-1, ofs=>12 },
	'1 破軍' => { cw=>-1, ofs=> 4 },
    };
    foreach (keys %$main_star) {
	$st = exists $morph{$_} ? "$_化$morph{$_}" : $_;
	push @{ $chart->{($main_star->{$_}{cw}*$ms + $main_star->{$_}{ofs}+12) % 12}{star} }, $st;
    }
    # 安干系諸星
    my ($heaven_star) = {
	'1 祿存' => [ 1, 3, 4, 6, 7, 6, 7, 9, 10, 0 ],
	'1 擎羊' => [ 2, 4, 5, 7, 8, 7, 8, 10, 11, 1 ],
	'1 陀羅' => [ 0, 2, 3, 5, 6, 5, 6, 8, 9, 11 ],
	'1 天魁' => [ 4, 2, 1, 0, 0, 2, 1, 2, 7, 4 ],
	'1 天越' => [ 6, 8, 9, 10, 10, 8, 9, 8, 3, 6 ],
	'4 天官' => [ 7, 8, 5, 6, 3, 4, 10, 0, 10, 11 ],
	'4 天福' => [ 6, 10, 9, 1, 0, 4, 3, 7, 6, 7 ],
	'3 天廚' => [ 0, 6, 7, 1, 6, 7, 9, 3, 7, 10 ],
    };
    foreach (keys %$heaven_star) {
	push @{ $chart->{$heaven_star->{$_}[$person->{heaven}]}{star} }, $_;
    }
    # 安月系諸星
    push @{ $chart->{($person->{month} + 4) % 12}{star} }, '1 左輔';
    push @{ $chart->{(12 - $person->{month}) % 12}{star} }, '1 右弼';
    push @{ $chart->{($person->{month} + 9) % 12}{star} }, '2 天刑';
    push @{ $chart->{($person->{month} + 1) % 12}{star} }, '2 天姚';

    push @{ $chart->{(7,9,11,1,3,5,7)[int(($person->{month}+1)/2)]}{star} }, '3 解神';
    push @{ $chart->{(3,6,9,0)[$person->{month} % 4]}{star} }, '3 天巫';
    push @{ $chart->{(3,11,6,5,3,8,4,0,8,3,7,11)[$person->{month}]}{star} }, '3 天月';
    push @{ $chart->{(3,1,11,9,7,5)[$person->{month} % 6]}{star} }, '3 陰煞';
    # 安時系諸星
    my ($hour_star) = {
	'1 文昌' => { cw=>-1, ofs=> 0 },
	'1 文曲' => { cw=> 1, ofs=> 4 },
	'1 地劫' => { cw=> 1, ofs=>-1 },
	'1 空劫' => { cw=>-1, ofs=> 1 },
	'3 臺輔' => { cw=> 1, ofs=> 6 },
	'3 封誥' => { cw=> 1, ofs=> 2 },
    };
    foreach (keys %$hour_star) {
	$st = exists $morph{$_} ? "$_化$morph{$_}" : $_;
	push @{ $chart->{($hour_star->{$_}{cw}*$person->{hour} + $hour_star->{$_}{ofs}+12)%12}{star} }, $st;
    }
    push @{ $chart->{ ($person->{hour}+(9,2,3,1)[$person->{earth} % 4]) % 12 }{star} }, '1 火星';
    push @{ $chart->{ ($person->{hour}+(10,10,10,3)[$person->{earth} % 4]) % 12 }{star} }, '1 鈴星';
    # 安支系諸星
    my ($earth_star) = {
	'3 天空' => { cw=> 1, ofs=> 1 },
	'3 天哭' => { cw=>-1, ofs=> 8 },
	'3 天虛' => { cw=> 1, ofs=> 6 },
	'3 龍池' => { cw=> 1, ofs=> 4 },
	'3 鳳閣' => { cw=>-1, ofs=>12 },
	'3 紅鸞' => { cw=>-1, ofs=> 5 },
	'3 天喜' => { cw=>-1, ofs=>11 },
	'3 天德' => { cw=> 1, ofs=> 9 },
	'3 月德' => { cw=> 1, ofs=> 5 },
    };
    foreach (keys %$earth_star) {
	push @{ $chart->{($earth_star->{$_}{cw}*$person->{earth} + $earth_star->{$_}{ofs}+12)%12}{star} }, $_;
    }
    push @{ $chart->{ (18-$person->{earth}%4*3) % 12 }{star} }, '1 天馬';
    push @{ $chart->{ (int($person->{earth}/3)*3+3) % 12 }{star} }, '3 孤辰';
    push @{ $chart->{ (int($person->{earth}/3)*3+11) % 12 }{star} }, '3 寡宿';
    push @{ $chart->{(2,9,10,11,6,7,8,3,4,5,0,1)[$person->{earth}]}{star} }, '3 蜚廉';
    push @{ $chart->{ (22-$person->{earth}%3*4) % 12 }{star} }, '3 破碎';
    push @{ $chart->{ (20-$person->{earth}%4*3) % 12 }{star} }, '3 華蓋'; # '
    push @{ $chart->{ (13-$person->{earth}%4*3) % 12 }{star} }, '3 咸池';
    push @{ $chart->{ ($chart->{fate}+$person->{earth}+11) % 12 }{star} }, '3 天才';
    push @{ $chart->{ ($chart->{body}+$person->{earth}+11) % 12 }{star} }, '3 天壽';

    # Gemini 補充4級星：
    push @{ $chart->{ ($person->{earth} + 9) % 12 }{star} }, '4 年解';

    # 各宮按星等排序
    for ($e=0; $e<12; ++$e) {
	@{ $chart->{$e}{star} } = exists $chart->{$e}{star} ? sort @{ $chart->{$e}{star} } : ();
    }
    return $chart;
}

$bad = 0;
foreach (@ARGV) {
    $bad = 1 if not (/^\d+$/);
}
if ($#ARGV != 4 or $bad) {
    print STDERR <<eof;
    使用範例: 以農曆生辰為甲寅年5月7日申時為例, 請下
    perl ZiWeiDouShu.pl 1 3 5 7 9
eof
    exit 1;
}

$person = {
    heaven => $ARGV[0] % 10,
    earth => $ARGV[1] % 12,
    month => $ARGV[2] % 12,
    day => $ARGV[3],
    hour => $ARGV[4] % 12,
};

my ($chart) = create_chart($person);
display_chart($chart);
# print Dumper($chart);
list_chart($chart);

