# -*- coding: utf-8 -*-
"""把改动过的页面推给百度（普通收录 API）和 IndexNow（必应等）。
用法：
  python3 工具/push_index.py docs/guide/today.html docs/index.html ...   # 按文件推
  python3 工具/push_index.py --changed BASE_SHA HEAD_SHA                  # 按 git 改动推（GitHub Actions 用）
百度 token 从环境变量 BAIDU_TOKEN 读（GitHub 仓库 Secrets），没有就跳过百度。
百度每天配额很少（约 10 条），一次最多推 BAIDU_MAX 条，多出来的打印出来、不推。
IndexNow 的 key 文件是 docs/ 下那个 32 位十六进制命名的 .txt。
"""
import glob, json, os, re, subprocess, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://youfuhaishu.com'
BAIDU_MAX = 5
SKIP = re.compile(r'(^|/)baidu_verify_|^docs/fz/credits\.html$')


def to_url(path):
    rel = path[len('docs/'):]
    if rel.endswith('index.html'):
        rel = rel[:-len('index.html')]
    return SITE + '/' + rel


def changed(base, head):
    if not base or set(base) == {'0'}:
        return []
    out = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=AM', base, head, '--', 'docs/'],
                         capture_output=True, text=True, cwd=REPO).stdout.split('\n')
    return [p for p in out if p.endswith('.html')]


def post(url, body, ctype):
    req = urllib.request.Request(url, data=body.encode('utf-8'), headers={'Content-Type': ctype})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def main(argv):
    files = changed(argv[1], argv[2]) if argv and argv[0] == '--changed' else argv
    files = [f for f in files if f.startswith('docs/') and f.endswith('.html') and not SKIP.search(f)]
    # 每日页最后推，配额紧的时候先推新内容
    files.sort(key=lambda f: f.endswith('guide/today.html'))
    urls = list(dict.fromkeys(to_url(f) for f in files))
    if not urls:
        print('没有要推的页面')
        return
    print('要推的页面：', *urls, sep='\n  ')

    token = os.environ.get('BAIDU_TOKEN', '').strip()
    if token:
        batch, rest = urls[:BAIDU_MAX], urls[BAIDU_MAX:]
        code, text = post(f'http://data.zz.baidu.com/urls?site={SITE}&token={token}', '\n'.join(batch), 'text/plain')
        print('百度', code, text)
        if rest:
            print('百度配额有限，这次没推：', *rest, sep='\n  ')
    else:
        print('没有 BAIDU_TOKEN，跳过百度')

    keys = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(REPO, 'docs', '*.txt'))
            if re.fullmatch(r'[0-9a-f]{32}\.txt', os.path.basename(p))]
    if keys:
        body = json.dumps({'host': 'youfuhaishu.com', 'key': keys[0],
                           'keyLocation': f'{SITE}/{keys[0]}.txt', 'urlList': urls})
        code, text = post('https://api.indexnow.org/indexnow', body, 'application/json; charset=utf-8')
        print('IndexNow', code, text or '(ok)')


if __name__ == '__main__':
    main(sys.argv[1:])
