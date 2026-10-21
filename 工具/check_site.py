# -*- coding: utf-8 -*-
"""网站体检：站内死链、超大图片、漏了统计代码的页面、sitemap 漏收的页面。
有问题就打印出来并以退出码 1 结束（GitHub Actions 会标红并发邮件）。
用法：python3 工具/check_site.py
"""
import glob, os, re, sys
from urllib.parse import unquote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')
SITE = 'https://youfuhaishu.com/'
IMG_MAX_KB = 800
# 不需要统计代码、不进 sitemap 的页面
NOT_PAGES = re.compile(r'(^|/)baidu_verify_')
NO_SITEMAP_OK = re.compile(r'^(fz/credits|404)\.html$')

problems = []
pages = sorted(os.path.relpath(p, DOCS) for p in glob.glob(os.path.join(DOCS, '**', '*.html'), recursive=True))
pages = [p for p in pages if not NOT_PAGES.search(p)]
sitemap = open(os.path.join(DOCS, 'sitemap.xml'), encoding='utf-8').read()

for page in pages:
    html = open(os.path.join(DOCS, page), encoding='utf-8').read()
    if 'hm.baidu.com/hm.js' not in html or 'googletagmanager.com/gtag' not in html:
        problems.append(f'漏了统计代码：{page}')
    url = SITE + (page[:-len('index.html')] if page.endswith('index.html') else page)
    if f'<loc>{url}</loc>' not in sitemap and not NO_SITEMAP_OK.search(page):
        problems.append(f'sitemap 没收：{page}')
    for ref in re.findall(r'(?:href|src|poster|data-src-m)="([^"]+)"', html):
        if re.match(r'(https?:|mailto:|tel:|data:|javascript:|#|//)', ref):
            continue
        path = unquote(ref.split('#')[0].split('?')[0])
        if not path:
            continue
        base = DOCS if path.startswith('/') else os.path.dirname(os.path.join(DOCS, page))
        target = os.path.normpath(os.path.join(base, path.lstrip('/')))
        if os.path.isdir(target):
            target = os.path.join(target, 'index.html')
        if not os.path.exists(target):
            problems.append(f'死链：{page} → {ref}')

for name in open(os.path.join(REPO, '工具', 'hero_photos.txt'), encoding='utf-8'):
    name = name.strip()
    if name and not name.startswith('#') and not os.path.exists(os.path.join(DOCS, 'img', name)):
        problems.append(f'首页轮换照片不存在：工具/hero_photos.txt 里的 {name}')

for img in glob.glob(os.path.join(DOCS, '**', '*.*'), recursive=True):
    if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and os.path.getsize(img) > IMG_MAX_KB * 1024:
        problems.append(f'图片太大（{os.path.getsize(img) // 1024}KB，建议 {IMG_MAX_KB}KB 以内）：{os.path.relpath(img, DOCS)}')

print(f'检查了 {len(pages)} 个页面')
for p in problems:
    print(' -', p)
if problems:
    sys.exit(1)
print('全部正常')
