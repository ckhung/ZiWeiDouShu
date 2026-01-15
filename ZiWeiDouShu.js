const heavenNames = ['癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬'];
const earthNames = ['亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌'];
const houseNames = ['命宮', '兄弟', '夫妻', '子女', '財帛', '疾厄', '遷移', '僕役', '官祿', '田宅', '福德', '父母'];

function init() {
    const fill = (id, list, suffix="") => {
        const s = document.getElementById(id);
        list.forEach((v, i) => s.add(new Option(v + suffix, i)));
    };
    fill('heaven', heavenNames);
    fill('earth', earthNames);
    fill('hour', earthNames, "時");
    for(let i=1; i<=12; i++) document.getElementById('month').add(new Option(i + "月", i));
    for(let i=1; i<=30; i++) document.getElementById('day').add(new Option(i + "日", i));
}

// 輔助函式：確保取模運算在負數時也能正確運作 (同 Perl 邏輯)
const fixMod = (n, m) => ((n % m) + m) % m;

function findElement(fate, heaven) {
    // 定五行局； 2026參考資料： https://www.ai5429.com/c/505.htm
    // 輸入： 命宮支、生年干
    const elem = [4, 2, 6, 5, 3];
    const ofs = [1, 0, 1, 3, 2, 4];
    
    let t = ofs[Math.floor((fate + 1) / 2) % 6];
    // 命宮支 戌亥=>1、 子丑=>0、 ... 那一欄等同於 「子丑欄向下位移」 幾格
    return elem[(t + heaven) % 5];
    // 生年干 甲己=>1=>水二局
}

/*
for (let heaven = 1; heaven <= 5; ++heaven) {
    let row = "";
    for (let fate = 1; fate <= 12; ++fate) {
        row += findElement(fate, heaven) + " ";
    }
    console.log(row.trim());
}
*/

function createChart(p) {
    let chart = { person: p };
    for (let i = 0; i < 12; i++) chart[i] = { star: [] };

    let head = fixMod((p.heaven % 5) * 2 + 1, 10);
    for (let e = 0; e < 12; e++) chart[fixMod(e + 3, 12)].heaven = fixMod(e + head, 10);

    chart.body = fixMod(p.month + p.hour + 1, 12);
    chart.fate = fixMod(p.month - p.hour + 15, 12);

    for (let e = 0; e < 12; e++) chart[fixMod(chart.fate - e, 12)].house = e;

    // 定五行局
    t = findElement(chart.fate, p.heaven);
    chart.element = ['', '', '水二', '木三', '金四', '土五', '火六'][t];

    const mTransform = [
        ["破軍", "巨門", "太陰", "貪狼"], ["廉貞", "破軍", "武曲", "太陽"], ["天機", "天梁", "紫微", "太陰"],
        ["天同", "天機", "文昌", "廉貞"], ["太陰", "天同", "天機", "巨門"], ["貪狼", "太陰", "右弼", "天機"],
        ["武曲", "貪狼", "天梁", "文曲"], ["太陽", "武曲", "天同", "太陰"], ["巨門", "太陽", "文曲", "文昌"],
        ["天梁", "紫微", "左輔", "武曲"]
    ];
    let morph = {};
    const tags = ['祿', '權', '科', '忌'];
    mTransform[p.heaven].forEach((s, i) => morph['1 ' + s] = '1 ' + s + '化' + tags[i]);
    // 為避免遺漏紫微、左輔、右弼， 晚一點再處理四化

    let ms = fixMod(6 - p.day, t);
    ms = [3, 2, 5, 0, 7, -2][ms];
    ms = fixMod(Math.floor((p.day - 1) / t) + ms, 12);
    chart[ms].star.push('1 紫微');

    const mainStars = {
        '1 天機': {cw:1, ofs:-1}, '1 太陽': {cw:1, ofs:-3}, '1 武曲': {cw:1, ofs:-4}, '1 天同': {cw:1, ofs:-5},
        '1 廉貞': {cw:1, ofs:4}, '1 天府': {cw:-1, ofs:6}, '1 太陰': {cw:-1, ofs:7}, '1 貪狼': {cw:-1, ofs:8},
        '1 巨門': {cw:-1, ofs:9}, '1 天相': {cw:-1, ofs:10}, '1 天梁': {cw:-1, ofs:11}, '1 七殺': {cw:-1, ofs:12},
        '1 破軍': {cw:-1, ofs:4}
    };
    for (let s in mainStars) {
        chart[fixMod(mainStars[s].cw * ms + mainStars[s].ofs, 12)].star.push(s);
    }

    // 安干系
    const hStars = {
        '1 祿存': [1,3,4,6,7,6,7,9,10,0], '1 擎羊': [2,4,5,7,8,7,8,10,11,1], '1 陀羅': [0,2,3,5,6,5,6,8,9,11],
        '1 天魁': [4,2,1,0,0,2,1,2,7,4], '1 天越': [6,8,9,10,10,8,9,8,3,6], '4 天官': [7,8,5,6,3,4,10,0,10,11],
        '4 天福': [6,10,9,1,0,4,3,7,6,7], '3 天廚': [0,6,7,1,6,7,9,3,7,10]
    };
    for (let s in hStars) chart[hStars[s][p.heaven]].star.push(s);

    // 安月系
    chart[fixMod(p.month + 4, 12)].star.push('1 左輔');
    chart[fixMod(12 - p.month, 12)].star.push('1 右弼');
    chart[fixMod(p.month + 9, 12)].star.push('2 天刑');
    chart[fixMod(p.month + 1, 12)].star.push('2 天姚');
    chart[[7,9,11,1,3,5,7][Math.floor((p.month+1)/2)]].star.push('3 解神');
    chart[[3,6,9,0][p.month % 4]].star.push('3 天巫');
    chart[[3,11,6,5,3,8,4,0,8,3,7,11][p.month]].star.push('3 天月');
    chart[[3,1,11,9,7,5][p.month % 6]].star.push('3 陰煞');

    // 安時系
    const hrStars = {
        '1 文昌': {cw:-1, ofs:0}, '1 文曲': {cw:1, ofs:4}, '1 地劫': {cw:1, ofs:-1}, '1 空劫': {cw:-1, ofs:1},
        '3 臺輔': {cw:1, ofs:6}, '3 封誥': {cw:1, ofs:2}
    };
    for (let s in hrStars) {
        chart[fixMod(hrStars[s].cw * p.hour + hrStars[s].ofs, 12)].star.push(s);
    }
    chart[fixMod(p.hour + [9,2,3,1][p.earth % 4], 12)].star.push('1 火星');
    chart[fixMod(p.hour + [10,10,10,3][p.earth % 4], 12)].star.push('1 鈴星');

    for (let i = 0; i < 12; i++) {
	chart[i].star = chart[i].star.map(st => {
	    return (st in morph) ? morph[st] : st;
	});
    }

    // 安支系諸星
    const eStars = {
        '3 天空': {cw:1, ofs:1}, '3 天哭': {cw:-1, ofs:8}, '3 天虛': {cw:1, ofs:6}, '3 龍池': {cw:1, ofs:4},
        '3 鳳閣': {cw:-1, ofs:12}, '3 紅鸞': {cw:-1, ofs:5}, '3 天喜': {cw:-1, ofs:11}, '3 天德': {cw:1, ofs:9},
        '3 月德': {cw:1, ofs:5}
    };
    for (let s in eStars) chart[fixMod(eStars[s].cw * p.earth + eStars[s].ofs, 12)].star.push(s);
    chart[fixMod(18 - (p.earth % 4) * 3, 12)].star.push('1 天馬');
    chart[fixMod(Math.floor(p.earth/3)*3 + 3, 12)].star.push('3 孤辰');
    chart[fixMod(Math.floor(p.earth/3)*3 + 11, 12)].star.push('3 寡宿');
    chart[[2,9,10,11,6,7,8,3,4,5,0,1][p.earth]].star.push('3 蜚廉');
    chart[fixMod(22 - (p.earth % 3) * 4, 12)].star.push('3 破碎');
    chart[fixMod(20 - (p.earth % 4) * 3, 12)].star.push('3 華蓋');
    chart[fixMod(13 - (p.earth % 4) * 3, 12)].star.push('3 咸池');
    chart[fixMod(chart.fate + p.earth + 11, 12)].star.push('3 天才');
    chart[fixMod(chart.body + p.earth + 11, 12)].star.push('3 天壽');
    chart[fixMod(p.earth + 9, 12)].star.push('4 年解');

    for (let i = 0; i < 12; i++) chart[i].star.sort();
    return chart;
}

function drawVerticalText(ctx, text, x, y, fontSize) {
    ctx.font = fontSize + "px 'Microsoft JhengHei'";
    for (let i = 0; i < text.length; i++) {
        ctx.fillText(text[i], x, y + i * (fontSize + 2));
    }
}

function renderChart(chart) {
    const canvas = document.getElementById('ziweiCanvas');
    const ctx = canvas.getContext('2d');
    const cw = 200, ch = 200;
    const posMap = [[3,3],[3,2],[3,1],[3,0],[2,0],[1,0],[0,0],[0,1],[0,2],[0,3],[1,3],[2,3]];

    ctx.clearRect(0, 0, 800, 800);
    ctx.strokeStyle = "#333";

    // 畫網格
    for(let r=0; r<4; r++) {
        for(let c=0; c<4; c++) {
            if (r > 0 && r < 3 && c > 0 && c < 3) continue;
            ctx.strokeRect(c * cw, r * ch, cw, ch);
        }
    }

    posMap.forEach((p, e) => {
        let x = p[1] * cw, y = p[0] * ch;

        // 宮位天干地支
        ctx.fillStyle = "#888";
        ctx.font = "16px Arial";
        ctx.fillText(heavenNames[chart[e].heaven] + earthNames[e], x + cw - 45, y + ch - 15);
        ctx.fillStyle = "#000";
        ctx.font = "bold 16px Arial";
        ctx.fillText(houseNames[chart[e].house], x + cw/2 - 15, y + ch - 15);
        if (chart.body === e) {
            ctx.fillStyle = "#d9534f";
            ctx.fillText("(身)", x + cw/2 - 45, y + ch - 15);
        }

        // 星曜繪製 (向下調整約半個字高度：y + 25)
        chart[e].star.forEach((s, i) => {
            let cleanName = s.replace(/^[0-9\s]*/, "");
            // 主星 (Level 1) 用藍色，其餘分類
            if (s.startsWith('1')) ctx.fillStyle = "#0000FF"; // 藍色
            else if (s.startsWith('2')) ctx.fillStyle = "#CC0000"; // 深紅
            else ctx.fillStyle = "#000"; // 黑色

            drawVerticalText(ctx, cleanName, x + cw - 25 - (i * 20), y + 25, 15);
        });
    });

    // 中央資訊
    ctx.fillStyle = "#000";
    ctx.font = "bold 22px Arial";
    let p = chart.person;
    ctx.fillText(`${heavenNames[p.heaven]}${earthNames[p.earth]}年 ${p.month}月${p.day}日${p.hour}時生`, 290, 380);
    ctx.fillText(`${chart.element}局`, 370, 420);
}

function listChart(chart) {
    const p = chart.person;
    let output = "";

    output += `${heavenNames[p.heaven]}${earthNames[p.earth]}年${p.month}月${p.day}日${earthNames[p.hour]}時生 ${chart.element}局\n`;
    output += `命宮 ${earthNames[chart.fate]} / 身宮 ${earthNames[chart.body]}\n---`;
    for (let i = 0; i < 12; i++) {
        let stars = chart[i].star.map(s => s.replace(/^[0-9\s]*/, "")).join(" ");
        output += `\n${houseNames[chart[i].house]} ${earthNames[i]}: ${stars}`;
    }
    return output
}

function execute() {
    const p = {
        heaven: parseInt(document.getElementById('heaven').value),
        earth: parseInt(document.getElementById('earth').value),
        month: parseInt(document.getElementById('month').value),
        day: parseInt(document.getElementById('day').value),
        hour: parseInt(document.getElementById('hour').value)
    };
    chart = createChart(p);
    renderChart(chart);
    document.getElementById('star_listing').innerText = listChart(chart);
}

const isNode = typeof process !== 'undefined' && process.versions && process.versions.node;

if (isNode) {
    const args = process.argv.slice(2);
    if (args.length !== 5) {
        console.error("使用範例： 以農曆生辰為甲寅年5月7日申時為例： 請下\nnodejs ZiWeiDouShu.html 1 3 5 7 9");
        process.exit(1);
    }

    const p = {
        heaven: parseInt(args[0]) % 10,
        earth: parseInt(args[1]) % 12,
        month: parseInt(args[2]) % 12,
        day: parseInt(args[3]),
        hour: parseInt(args[4]) % 12
    };

    const chart = createChart(p);
    console.log(listChart(chart));
} else {
    init();
}
