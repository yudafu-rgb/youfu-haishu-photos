# -*- coding: utf-8 -*-
"""把 docs/sitemap.xml 里每个页面的 <lastmod> 改成这个页面最后一次提交的日期（北京时间）。
daily-today.yml 每天跑；需要完整的 git 历史（checkout 用 fetch-depth: 0）。
"""
import os, re, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SM = os.path.join(REPO, 'docs', 'sitemap.xml')
SITE = 'https://youfuhaishu.com/'


def last_date(path):
    out = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=format-local:%Y-%m-%d', '--', path],
                         capture_output=True, text=True, cwd=REPO, env={**os.environ, 'TZ': 'Asia/Shanghai'}).stdout
    return out.strip()


def fix(m):
    url, old = m.group(1), m.group(2)
    rel = url[len(SITE):]
    path = 'docs/' + (rel + 'index.html' if rel == '' or rel.endswith('/') else rel)
    new = last_date(path) if os.path.exists(os.path.join(REPO, path)) else ''
    return m.group(0).replace(old, new) if new and new > old else m.group(0)


s = open(SM, encoding='utf-8').read()
s2 = re.sub(r'<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>', fix, s)
open(SM, 'w', encoding='utf-8').write(s2)
print('sitemap 日期更新了', sum(a != b for a, b in zip(s.splitlines(), s2.splitlines())), '行')
