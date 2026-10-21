# -*- coding: utf-8 -*-
"""每日自动生成 docs/guide/today.html：琅岐未来 7 天的日出日落、天气、月相、农历和潮汛（大潮/中潮/小潮）。
由 .github/workflows/daily-today.yml 每天北京时间 0 点后运行；也可以手动 python3 工具/build_today.py。
日出日落按 NOAA 太阳位置公式计算；潮汛按农历日推算，不是精确潮时，页面上写明以潮汐表为准。
天气和潮时来自 Open-Meteo（免费、不用 key）；拿不到就不显示那一块，页面照常生成。
潮时是海洋模型的估算（计算点在琅岐东边海上），TIDE_PUBLISH 为 False 时只打印到日志，不上页面，
等和潮汐表对比几天确认准了再打开。
页头页脚取自 docs/guide/bishu.html，统计代码、悬浮微信、底部咨询条跟着一起更新。
"""
import datetime as dt, json, math, os, re, urllib.request
import ephem
from lunardate import LunarDate

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
LAT, LON = 26.063260, 119.637902  # WGS-84，龙鼓度假村
TZ = 8
URL = 'https://youfuhaishu.com/guide/today.html'
TIDE_PUBLISH = False
# 采摘季：(开始 月日, 结束 月日, 提示)。来源和核实情况见 物业信息.md「采摘」一节；新品种确认了月份再往这里加。
PICKING = [
    (620, 831, '<b>琅岐葡萄季</b>：6 月底早熟品种上市，7–8 月最多，岛上葡萄园可以采摘（开园时间、价格以果园为准）。'),
    (801, 930, '<b>龙眼季</b>：8–9 月度假村可以采龙眼，另外收费。'),
    (901, 1130, '<b>洛神花</b>红了：园子里的洛神花住客可以免费采摘。<a href="/guide/roselle.html">看看</a>'),  # 月份待房东确认
]
WMO = {0: '晴', 1: '晴', 2: '多云', 3: '阴', 45: '雾', 48: '雾', 51: '毛毛雨', 53: '毛毛雨', 55: '毛毛雨',
       56: '冻雨', 57: '冻雨', 61: '小雨', 63: '中雨', 65: '大雨', 66: '冻雨', 67: '冻雨', 71: '小雪', 73: '中雪',
       75: '大雪', 77: '雪', 80: '阵雨', 81: '阵雨', 82: '强阵雨', 85: '阵雪', 86: '阵雪', 95: '雷阵雨',
       96: '雷阵雨', 99: '雷阵雨'}
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


def fetch(url):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.load(r)
        except Exception as e:  # 网络不通就跳过，不影响其他内容
            err = e
    print('skip', url.split('?')[0], err)
    return None


def weather(today):
    j = fetch('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&timezone=Asia%%2FShanghai&forecast_days=7'
              '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max'
              % (LAT, LON))
    if not j:
        return {}
    d = j['daily']
    out = {}
    for i, day in enumerate(d['time']):
        wind = d['wind_speed_10m_max'][i]
        out[day] = dict(sky=WMO.get(d['weather_code'][i], '—'), hi=round(d['temperature_2m_max'][i]),
                        lo=round(d['temperature_2m_min'][i]), rain=d['precipitation_probability_max'][i],
                        windy=wind is not None and wind >= 39)  # 39 km/h 约 6 级
    return out


def tides(today):
    """海洋模型逐小时海面高度，取局部最高最低点，返回 {日期: [('高'/'低', 'HH:MM'), ...]}。"""
    j = fetch('https://marine-api.open-meteo.com/v1/marine?latitude=%s&longitude=%s&timezone=Asia%%2FShanghai'
              '&forecast_days=7&hourly=sea_level_height_msl' % (LAT, LON))
    if not j:
        return {}
    t, v = j['hourly']['time'], j['hourly']['sea_level_height_msl']
    out = {}
    for i in range(1, len(v) - 1):
        if None in (v[i - 1], v[i], v[i + 1]):
            continue
        kind = '高' if v[i] > v[i - 1] and v[i] >= v[i + 1] else '低' if v[i] < v[i - 1] and v[i] <= v[i + 1] else None
        if kind:
            out.setdefault(t[i][:10], []).append((kind, t[i][11:16]))
    return out


def moon(d):
    """当天月相名、亮面百分比、月出时间（北京时间）。"""
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(LAT), str(LON), 0
    start = dt.datetime(d.year, d.month, d.day) - dt.timedelta(hours=TZ)  # 北京时间 0 点
    obs.date = start
    m = ephem.Moon(start + dt.timedelta(hours=12))
    illum = round(m.phase)
    nxt_new = ephem.next_new_moon(start).datetime()
    prev_new = ephem.previous_new_moon(start).datetime()
    age = (start - prev_new).total_seconds() / 86400
    waxing = age < (nxt_new - prev_new).total_seconds() / 172800
    if illum >= 97:
        name = '满月'
    elif illum <= 3:
        name = '新月'
    elif illum >= 50:
        name = '盈凸月' if waxing else '亏凸月'
    else:
        name = '娥眉月' if waxing else '残月'
    try:
        rise = (obs.next_rising(ephem.Moon()).datetime() + dt.timedelta(hours=TZ))
        rise = rise.strftime('%H:%M') if rise.date() == d else '—'
    except ephem.CircumpolarError:
        rise = '—'
    return name, illum, rise


MOON_ICON = {'新月': '🌑', '娥眉月': '🌒', '盈凸月': '🌔', '满月': '🌕', '亏凸月': '🌖', '残月': '🌘'}


def moon_notes(today):
    """下一个满月（含月出）和临近的中秋，给页面上的「赏月」一段用。"""
    start = dt.datetime(today.year, today.month, today.day) - dt.timedelta(hours=TZ)
    full = (ephem.next_full_moon(start).datetime() + dt.timedelta(hours=TZ)).date()
    rise = moon(full)[2]
    out = [f"下一个满月在 {full.month} 月 {full.day} 日（周{WEEK[full.weekday()]}）"
           + (f"，月出 {rise}" if rise != '—' else '') + "。满月前后两三天，太阳下山后不久月亮就从海上升起，到门口沙滩看最好，海面上会有一条月光。"]
    ly = LunarDate.from_solar_date(today.year, today.month, today.day).year
    for y in (ly, ly + 1):
        mid = LunarDate(y, 8, 15).to_solar_date()
        if 0 <= (mid - today).days <= 90:
            out.append(f"今年中秋是 {mid.month} 月 {mid.day} 日（周{WEEK[mid.weekday()]}），想一家人在海边别墅过中秋赏月，建议提早订。")
            break
    return out


def lunar_to_solar(y, m, d):
    try:
        return LunarDate(y, m, d).to_solar_date()
    except ValueError:  # 腊月没有三十的年份
        return LunarDate(y, m, d - 1).to_solar_date() + dt.timedelta(days=1)


def md(d):
    return f"{d.month} 月 {d.day} 日"


def notices(today):
    """首页和每日页的「近期提示」：季节提醒 + 按农历自动算的节日活动。规则对应 物业信息.md。"""
    out, m = [], today.month
    ly = LunarDate.from_solar_date(today.year, today.month, today.day).year
    for y in (ly, ly + 1):
        eve = lunar_to_solar(y - 1, 12, 30)          # 除夕
        d10, d15, d26 = (lunar_to_solar(y, 1, k) for k in (10, 15, 26))
        if 0 <= (eve - today).days <= 45 or eve <= today <= d15:
            out.append(f'<b>春节</b>（除夕 {md(eve)} 至正月十五 {md(d15)}）房间最紧，建议提早订。<a href="/price.html">看房价</a>')
        if 0 <= (d10 - today).days <= 30:
            out.append(f'<b>潭头游神临近</b>：正月初十（{md(d10)}）长乐厚福村游神，从度假村开车约 30 分钟。<a href="/guide/chunjie.html">怎么去</a>')
        elif d10 < today <= d26:
            out.append(f'<b>正月二十六（{md(d26)}）</b>厚福村还有一场游神，人比初十少一些。<a href="/guide/chunjie.html">怎么去</a>')
        if 0 <= (d15 - today).days <= 15:
            out.append(f'<b>元宵（{md(d15)}）</b>：村里有游灯、舞龙舞狮。')
        mid = lunar_to_solar(y, 8, 15)
        if 0 <= (mid - today).days <= 30:
            out.append(f'<b>中秋（{md(mid)}）</b>：在海边别墅赏月，建议提早订。')
    if m == 12 or (m == 1 and today.day == 1):
        out.append('<b>元旦</b>按周末节假日价。<a href="/price.html">看房价</a>')
    start = dt.datetime(today.year, today.month, today.day) - dt.timedelta(hours=TZ)
    full = (ephem.next_full_moon(start).datetime() + dt.timedelta(hours=TZ)).date()
    if (full - today).days <= 2:
        out.append(f'<b>{md(full)} 满月</b>：傍晚到门口沙滩看月亮从海上升起。<a href="/guide/today.html">月出时间</a>')
    if m in (7, 8, 9):
        out.append('<b>暑期泳池</b>：度假村游乐场泳池 7–9 月开放，住客可用。')
    md_ = m * 100 + today.day
    for start, end, text in PICKING:
        if start <= md_ <= end:
            out.append(text)
    if m in (6, 7, 8, 9):
        out.append('<b>夏天海边晒</b>：记得防晒、带帽子，白天太晒就傍晚再去沙滩。')
    if m in (12, 1, 2):
        out.append('<b>冬天海边风大</b>：记得带件外套；屋里空调能开暖风，不冷。')
    out.append('今天几点日出日落、是不是大潮？<a href="/guide/today.html">看今日日出日落和潮汛</a>')
    return out


def write_daily_js(today):
    """docs/daily.js：首页同步加载，设定当天的大图（CSS 变量 --hero）和近期提示。不是 HTML，不会触发收录推送。"""
    photos = [l.strip() for l in open(os.path.join(REPO, '工具', 'hero_photos.txt'), encoding='utf-8')
              if l.strip() and not l.startswith('#') and os.path.exists(os.path.join(DOCS, 'img', l.strip()))]
    hero = photos[today.toordinal() % len(photos)] if photos else 'hero.jpg'
    js = ('// 由 工具/build_today.py 每天生成，不要手改\n'
          f'window.YF = {json.dumps({"date": today.isoformat(), "hero": "/img/" + hero, "notes": notices(today)}, ensure_ascii=False)};\n'
          'document.documentElement.style.setProperty("--hero", "url(" + window.YF.hero + ")");\n')
    open(os.path.join(DOCS, 'daily.js'), 'w', encoding='utf-8').write(js)


def day_info(d):
    ld = LunarDate.from_solar_date(d.year, d.month, d.day)
    rise, sset = sun_times(d)
    name, cls, note = tide_level(ld.day)
    return dict(d=d, lunar=('闰' if ld.is_leap_month else '') + CN_MON[ld.month - 1] + '月' + CN_DAY[ld.day - 1],
                rise=rise.strftime('%H:%M'), sset=sset.strftime('%H:%M'),
                gold=(sset - dt.timedelta(minutes=40)).strftime('%H:%M'), tide=name, cls=cls, note=note)


def build(today):
    days = [day_info(today + dt.timedelta(days=i)) for i in range(7)]
    wx, td = weather(today), tides(today)
    for x in days:
        x['wx'] = wx.get(x['d'].isoformat())
        x['tides'] = td.get(x['d'].isoformat(), [])
        print(x['d'], '潮时（模型估算）', ' '.join(k + v for k, v in x['tides']))
    mname, millum, mrise = moon(today)
    for x in days:
        x['micon'] = MOON_ICON[moon(x['d'])[0]]
    mnotes = moon_notes(today)
    w0 = days[0]['wx']
    t = days[0]
    big = [x for x in days if x['tide'] == '大潮']
    big_txt = ('、'.join(f"{x['d'].month}月{x['d'].day}日" for x in big) + ' 是大潮，想赶海挑这几天。') if big \
        else '这一周没有大潮，下一次大潮在农历初一或十五前后。'
    datestr = f"{today.year}年{today.month}月{today.day}日"
    title = f'琅岐今日日出日落、天气和赶海潮汛（{today.month}月{today.day}日更新）｜有福海墅'
    desc = (f"{datestr}（星期{WEEK[today.weekday()]}，农历{t['lunar']}）福州琅岐岛日出 {t['rise']}、日落 {t['sset']}，"
            + (f"{w0['sky']} {w0['lo']}–{w0['hi']}℃，" if w0 else '') +
            f"今天{t['tide']}。未来 7 天日出日落、天气和赶海潮汛，每天自动更新。")

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
.tag.big{background:#ffd34d;color:#1d2a33}.warn{color:#c0392b}.tag.mid{background:rgba(0,0,0,.07)}.tag.small{background:rgba(0,0,0,.03)}
</style>
</head>''')

    rows = '\n'.join(
        f"<tr><td>{x['d'].month}/{x['d'].day} 周{WEEK[x['d'].weekday()]}</td><td>{x['lunar']} {x['micon']}</td>"
        f"<td>{x['rise']}</td><td>{x['sset']}</td>"
        + (f"<td>{x['wx']['sky']} {x['wx']['lo']}–{x['wx']['hi']}℃" + (f"<br><span class=\"warn\">降雨 {x['wx']['rain']}%</span>" if (x['wx']['rain'] or 0) >= 50 else '') + "</td>" if x['wx'] else ('<td>—</td>' if wx else ''))
        + f"<td><span class=\"tag {x['cls']}\">{x['tide']}</span>"
        + ('<br>' + ' '.join(k + v for k, v in x['tides'] if k == '低') + ' 低潮' if TIDE_PUBLISH and x['tides'] else '')
        + "</td></tr>" for x in days)
    body = f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">游玩攻略</a></p>
    <h1>琅岐今日日出日落、天气和赶海潮汛</h1>
    <p>{datestr}，星期{WEEK[today.weekday()]}，农历{t['lunar']}。本页每天自动更新，住在龙鼓度假村的客人可以照着安排看日出日落、赶海。</p>

    <div class="today">
      <div><span>日出</span><b>{t['rise']}</b></div>
      <div><span>日落</span><b>{t['sset']}</b></div>
      <div><span>拍照最好看</span><b>{t['gold']}</b><span>日落前约 40 分钟</span></div>
      <div><span>今天潮汛</span><b>{t['tide']}</b></div>
      {f"<div><span>天气</span><b>{w0['sky']}</b><span>{w0['lo']}–{w0['hi']}℃，降雨概率 {w0['rain']}%" + ('，风大' if w0['windy'] else '') + "</span></div>" if w0 else ''}
      <div><span>月相</span><b>{mname}</b><span>亮面 {millum}%{'，月出 ' + mrise if mrise != '—' else ''}</span></div>
    </div>
    <p>今天{t['tide']}：{t['note']}。</p>

<h2>近期提示</h2>
<ul>{''.join(f"<li>{n}</li>" for n in notices(today)[:-1]) or '<li>最近没有特别的活动，海边看日出日落、赶海就很好。</li>'}</ul>

<h2>未来 7 天</h2>
<table class="week">
<tr><th>日期</th><th>农历</th><th>日出</th><th>日落</th>{'<th>天气</th>' if wx else ''}<th>潮汛</th></tr>
{rows}
</table>
<p>{big_txt}</p>

<h2>赏月</h2>
{''.join(f"<p>{n}</p>" for n in mnotes)}

<h2>怎么用这张表</h2>
<ul>
  <li><strong>看日出：</strong>度假村门口的沙滩就能看海上日出，出门走几步，很壮观。想登高看，<a href="bishu.html">白云山观日台</a>也是福州一带看日出的好地方，从度假村开车约 20 分钟，天没亮也能开到观日台附近。</li>
  <li><strong>看日落：</strong>日落前半小时到门口沙滩或山顶，<a href="sunset.html">看日落的几个地方</a>。</li>
  <li><strong>赶海：</strong>大潮日退得最远。具体几点退潮，出发前在天气 App 搜「琅岐 潮汐」，退潮前后两小时最合适。<a href="ganhai.html">赶海攻略</a></li>
  <li><strong>安全：</strong>涨潮很快，看到水开始往回漫就上岸；礁石滑，穿防滑鞋。</li>
</ul>
<p style="font-size:14px;opacity:.7">日出日落、月相按龙鼓度假村坐标计算，误差一两分钟。天气来自 Open-Meteo 预报，出发前再看一眼手机天气。潮汛按农历推算，只表示潮水大小，不是精确潮时，以潮汐表为准。</p>

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
    write_daily_js(today)

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
