# -*- coding: utf-8 -*-
"""每日自动生成 docs/guide/today.html：琅岐未来 7 天的日出日落、农历和潮汛（大潮/中潮/小潮）。
由 .github/workflows/daily-today.yml 每天北京时间 0 点后运行；也可以手动 python3 工具/build_today.py。
日出日落按 NOAA 太阳位置公式计算；潮汛按农历日推算，不是精确潮时，页面上写明以潮汐表为准。
页头页脚取自 docs/guide/bishu.html，统计代码、悬浮微信、底部咨询条跟着一起更新。
"""
import datetime as dt, math, os, re
from lunardate import LunarDate

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
LAT, LON = 26.063260, 119.637902  # WGS-84，龙鼓度假村
TZ = 8
URL = 'https://youfuhaishu.com/guide/today.html'
WEEK = '一二三四五六日'
CN_DAY = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
          '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
CN_MON = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']


def sun_times(d):
    """返回 (日出, 日落) 的北京时间 datetime。NOAA 简化算法，误差 1–2 分钟。"""
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lat = math.radians(LAT)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl))
                                - math.tan(lat) * math.tan(decl)))
    base = dt.datetime(d.year, d.month, d.day)
    rise = base + dt.timedelta(minutes=720 - 4 * (LON + ha) - eqt + TZ * 60)
    sset = base + dt.timedelta(minutes=720 - 4 * (LON - ha) - eqt + TZ * 60)
    return rise, sset


def tide_level(lday):
    """按农历日推算潮汛。潮汐比月相晚一两天，所以大潮落在初一到初四、十五到十九。"""
    if lday in (1, 2, 3, 4, 15, 16, 17, 18, 19, 30):
        return '大潮', 'big', '退得最远，滩涂露出最多，赶海收获最好'
    if lday in (7, 8, 9, 10, 22, 23, 24, 25):
        return '小潮', 'small', '涨落小，滩涂露得少，适合带小孩在浅滩玩沙'
    return '中潮', 'mid', '退潮后也能下滩，就是没有大潮露得多'


def day_info(d):
    ld = LunarDate.from_solar_date(d.year, d.month, d.day)
    rise, sset = sun_times(d)
    name, cls, note = tide_level(ld.day)
    return dict(d=d, lunar=('闰' if ld.is_leap_month else '') + CN_MON[ld.month - 1] + '月' + CN_DAY[ld.day - 1],
                rise=rise.strftime('%H:%M'), sset=sset.strftime('%H:%M'),
                gold=(sset - dt.timedelta(minutes=40)).strftime('%H:%M'), tide=name, cls=cls, note=note)


def build(today):
    days = [day_info(today + dt.timedelta(days=i)) for i in range(7)]
    t = days[0]
    big = [x for x in days if x['tide'] == '大潮']
    big_txt = ('、'.join(f"{x['d'].month}月{x['d'].day}日" for x in big) + ' 是大潮，想赶海挑这几天。') if big \
        else '这一周没有大潮，下一次大潮在农历初一或十五前后。'
    datestr = f"{today.year}年{today.month}月{today.day}日"
    title = f'琅岐今日日落和赶海潮汛（{today.month}月{today.day}日更新）｜有福海墅'
    desc = (f"{datestr}（星期{WEEK[today.weekday()]}，农历{t['lunar']}）福州琅岐岛日出 {t['rise']}、日落 {t['sset']}，"
            f"今天{t['tide']}。未来 7 天日落时间和赶海潮汛，每天自动更新。")

    src = open(os.path.join(DOCS, 'guide', 'bishu.html'), encoding='utf-8').read()
    head, rest = src.split('<main class="article">', 1)
    tail = rest.split('</main>', 1)[1]
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + desc, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>琅岐今日日落和赶海潮汛', head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + desc, head)
    head = head.replace('https://youfuhaishu.com/guide/bishu.html', URL).replace('img/beach.jpg', 'img/dusk.jpg')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, flags=re.S)
    head = head.replace('</head>', '''<style>
.today{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:18px 0 8px}
.today div{border:1px solid rgba(0,0,0,.1);border-radius:10px;padding:12px 14px}
.today b{display:block;font-size:26px;line-height:1.2}
.today span{font-size:14px;opacity:.7}
table.week{width:100%;border-collapse:collapse;font-size:15px}
table.week th,table.week td{padding:8px 6px;border-bottom:1px solid rgba(0,0,0,.08);text-align:left}
.tag{display:inline-block;padding:1px 8px;border-radius:999px;font-size:13px}
.tag.big{background:#ffd34d;color:#1d2a33}.tag.mid{background:rgba(0,0,0,.07)}.tag.small{background:rgba(0,0,0,.03)}
</style>
</head>''')

    rows = '\n'.join(
        f"<tr><td>{x['d'].month}/{x['d'].day} 周{WEEK[x['d'].weekday()]}</td><td>{x['lunar']}</td>"
        f"<td>{x['sset']}</td><td><span class=\"tag {x['cls']}\">{x['tide']}</span></td></tr>" for x in days)
    body = f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">游玩攻略</a></p>
    <h1>琅岐今日日落和赶海潮汛</h1>
    <p>{datestr}，星期{WEEK[today.weekday()]}，农历{t['lunar']}。本页每天自动更新，住在龙鼓度假村的客人可以照着安排看日落、赶海。</p>

    <div class="today">
      <div><span>日出</span><b>{t['rise']}</b></div>
      <div><span>日落</span><b>{t['sset']}</b></div>
      <div><span>拍照最好看</span><b>{t['gold']}</b><span>日落前约 40 分钟</span></div>
      <div><span>今天潮汛</span><b>{t['tide']}</b></div>
    </div>
    <p>今天{t['tide']}：{t['note']}。</p>

<h2>未来 7 天</h2>
<table class="week">
<tr><th>日期</th><th>农历</th><th>日落</th><th>潮汛</th></tr>
{rows}
</table>
<p>{big_txt}</p>

<h2>怎么用这张表</h2>
<ul>
  <li><strong>看日落：</strong>日落前半小时到门口沙滩或山顶，<a href="sunset.html">看日落的几个地方</a>。</li>
  <li><strong>赶海：</strong>大潮日退得最远。具体几点退潮，出发前在天气 App 搜「琅岐 潮汐」，退潮前后两小时最合适。<a href="ganhai.html">赶海攻略</a></li>
  <li><strong>安全：</strong>涨潮很快，看到水开始往回漫就上岸；礁石滑，穿防滑鞋。</li>
</ul>
<p style="font-size:14px;opacity:.7">日出日落按龙鼓度假村坐标计算，误差一两分钟。潮汛按农历推算，只表示潮水大小，不是精确潮时，以潮汐表为准。</p>

<aside class="stay">
  <h2>住在有福海墅</h2>
  <p>龙鼓度假村里的三栋海边别墅，出门就是沙滩，赶海、看日落都不用开车。可订单间，也可整栋包下。</p>
  <a class="btn solid" href="../#book">看怎么预订</a>
  <a class="btn line" href="../#rooms">看看房间</a>
</aside>

    <p class="next">相关：<a href="ganhai.html">福州赶海攻略：琅岐岛退潮后的海滩</a></p>
  </div>
</main>'''
    open(os.path.join(DOCS, 'guide', 'today.html'), 'w', encoding='utf-8').write(head + body + tail)

    sm = os.path.join(DOCS, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    line = f'  <url><loc>{URL}</loc><lastmod>{today.isoformat()}</lastmod><changefreq>daily</changefreq></url>\n'
    if URL in s:
        s = re.sub(r'  <url><loc>' + re.escape(URL) + r'</loc>.*?</url>\n', line, s)
    else:
        s = s.replace('</urlset>', line + '</urlset>')
    open(sm, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=TZ)))
    build(now.date())
    print('ok', now.date())
