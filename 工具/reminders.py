# -*- coding: utf-8 -*-
"""每天早上看今天有没有该提醒房东的事，有就开 Issue（GitHub 会发邮件）。由 .github/workflows/reminders.yml 运行。
提醒规则：
- 每周一：内容日历上这周该发哪篇、还有哪些待核实
- 每月 1 号：这个月岛上能摘什么（取自 build_today.py 的 PICKING），可以发小红书
- 除夕前 21 天：平台标题换春节版；正月结束（农历二月初一）：换回平时版（见 物业信息.md「标题写法」）
- 除夕前 10 天：查今年「两马同春」灯会地点，更新元宵文章
用法：python3 工具/reminders.py [YYYY-MM-DD]   # 不带日期就是北京时间今天；只打印不开 Issue 加 --dry
"""
import datetime as dt, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_today as bt  # 复用采摘清单和农历换算

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def calendar_rows():
    for line in open(os.path.join(REPO, '内容日历.md'), encoding='utf-8'):
        m = re.match(r'\|\s*(\d{2})/(\d{2})\s*\|(.*)\|\s*$', line)
        if m:
            yield int(m.group(1)), int(m.group(2)), [c.strip() for c in m.group(3).split('|')]


def reminders(today):
    out = []
    if today.weekday() == 0:
        for mo, d, cols in calendar_rows():
            # 日历只写月/日，取离今天最近的那一年
            when = min((dt.date(y, mo, d) for y in (today.year - 1, today.year, today.year + 1)),
                       key=lambda x: abs((x - today).days))
            if 0 <= (when - today).days <= 6:
                title, angle, words, check = (cols + [''] * 4)[:4]
                todo = '事实都核实过了，可以写。' if check.startswith('✅') or check.startswith('无') else f'还要先核实：{check}'
                out.append((f'本周该发：{title}（{mo}/{d}）',
                            f'内容日历上这周（{mo}/{d}）排的是：\n\n- 官网攻略：**{title}**\n- 小红书角度：{angle}\n- 关键词：{words}\n- {todo}\n\n'
                            '要写的话，跟 Claude 说「写内容日历这周那篇」就行。不写这周也没关系，关掉这条就好。'))
    if today.day == 1:
        names = [n for n, a, b, _, _ in bt.PICKING
                 if any(bt.in_season(today.month * 100 + d, a, b) for d in (1, 15, 28))]
        if names:
            out.append((f'{today.month} 月采摘：{"、".join(names)}',
                        f'这个月琅岐岛上能摘：{"、".join(names)}。\n\n可以拍点照片发小红书、朋友圈，'
                        f'官网采摘日历已经自动更新：https://youfuhaishu.com/guide/caizhai.html'))
    ly = bt.LunarDate.from_solar_date(today.year, today.month, today.day).year
    for y in (ly, ly + 1):
        eve = bt.lunar_to_solar(y, 1, 1) - dt.timedelta(days=1)
        if today == eve - dt.timedelta(days=21):
            out.append((f'平台标题换春节版（除夕 {eve.month}/{eve.day}）',
                        '离除夕还有三周，按 物业信息.md「标题写法」，美团、途家等平台的房源标题换成春节版，加上「春节看长乐游神」。'
                        f'\n\n今年正月初十游神是 {bt.md(bt.lunar_to_solar(y, 1, 10))}，正月二十六是 {bt.md(bt.lunar_to_solar(y, 1, 26))}。'))
        if today == eve - dt.timedelta(days=10):
            out.append(('查今年「两马同春」灯会在哪办',
                        '官方一般这时候公布今年「两马同春闹元宵」灯会的地点和时间（2024、2025 年在琅岐红光湖公园，2026 年在马尾船政）。'
                        '查到后告诉 Claude，更新元宵那篇和 物业信息.md。'))
        if today == bt.lunar_to_solar(y, 2, 1):
            out.append(('平台标题换回平时版', '正月过完了，美团、途家等平台的房源标题把「春节看长乐游神」去掉，换回平时版。'))
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--dry']
    today = dt.date.fromisoformat(args[0]) if args else \
        (dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))).date()
    for title, body in reminders(today):
        print('提醒：', title)
        if '--dry' not in sys.argv:
            with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as f:
                f.write(body)
            subprocess.run([sys.executable, os.path.join(REPO, '工具', 'issue.py'), 'open', title, f.name], check=True)
