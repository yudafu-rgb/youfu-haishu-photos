# -*- coding: utf-8 -*-
"""在本仓库开 / 关 GitHub Issue，用来给房东发提醒（GitHub 会发邮件）。GitHub Actions 里用，需要 GITHUB_TOKEN。
用法：
  python3 工具/issue.py open  "标题" 正文文件   # 同标题已开着就追加评论，不重复开
  python3 工具/issue.py close "标题" "关闭说明"  # 同标题开着就评论后关掉
"""
import json, os, sys, urllib.parse, urllib.request

REPO = os.environ.get('GITHUB_REPOSITORY', 'yudafu-rgb/youfu-haishu-photos')
TOKEN = os.environ['GITHUB_TOKEN']


def api(method, path, data=None):
    req = urllib.request.Request(f'https://api.github.com/repos/{REPO}{path}', method=method,
                                 data=json.dumps(data).encode() if data else None,
                                 headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def find_open(title):
    for it in api('GET', '/issues?state=open&labels=自动提醒&per_page=100'):
        if it['title'] == title:
            return it
    return None


def main(action, title, arg):
    found = find_open(title)
    if action == 'open':
        body = open(arg, encoding='utf-8').read()
        if found:
            api('POST', f"/issues/{found['number']}/comments", {'body': body})
            print('已有，追加评论', found['html_url'])
        else:
            it = api('POST', '/issues', {'title': title, 'body': body, 'labels': ['自动提醒']})
            print('新开', it['html_url'])
    elif action == 'close' and found:
        api('POST', f"/issues/{found['number']}/comments", {'body': arg})
        api('PATCH', f"/issues/{found['number']}", {'state': 'closed'})
        print('已关闭', found['html_url'])


if __name__ == '__main__':
    main(*sys.argv[1:4])
