# -*- coding: utf-8 -*-
"""检查新上传的照片、视频：带没带拍摄位置（GPS）和手机型号、文件是不是太大。由 upload-check.yml 在每次推送后运行。
用法：python3 工具/check_uploads.py BASE_SHA HEAD_SHA   # 打印问题，有问题时退出码 1
注意：文件一旦推上公开仓库，历史里就一直有。发现带位置的，最好在电脑上去掉位置信息后重新上传，再把旧文件删掉。
"""
import io, json, os, subprocess, sys, tempfile
from PIL import Image

IMG = ('.jpg', '.jpeg', '.png', '.heic', '.webp')
VID = ('.mp4', '.mov', '.m4v')
WARN_MB = 50  # GitHub 超过 50MB 会警告，超过 100MB 直接拒收


def git(*a, text=True):
    return subprocess.run(['git', *a], capture_output=True, text=text, check=True).stdout


def main(base, head):
    if not base or set(base) == {'0'}:
        return []
    files = [f for f in git('-c', 'core.quotepath=off', 'diff', '--name-only', '--diff-filter=AM', base, head).splitlines()
             if f.lower().endswith(IMG + VID)]
    problems = []
    for f in files:
        data = git('show', f'{head}:{f}', text=False)
        mb = len(data) / 1024 / 1024
        if mb > WARN_MB:
            problems.append(f'`{f}` 有 {mb:.0f}MB，太大了（GitHub 超过 100MB 会拒收，仓库也会越来越慢），建议压缩后再传')
        found = []
        if f.lower().endswith(IMG):
            try:
                ex = Image.open(io.BytesIO(data)).getexif()
                if ex.get_ifd(0x8825):
                    found.append('拍摄位置（GPS）')
                if ex.get(0x010F) or ex.get(0x0110):
                    found.append(f'手机型号（{ex.get(0x010F, "")} {ex.get(0x0110, "")}'.rstrip() + '）')
            except Exception:
                pass
        else:
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(f)[1]) as t:
                t.write(data)
                t.flush()
                out = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_entries',
                                      'format_tags:stream_tags', t.name], capture_output=True, text=True).stdout
            tags = json.loads(out or '{}')
            keys = {k.lower(): v for k, v in tags.get('format', {}).get('tags', {}).items()}
            if any('location' in k or 'gps' in k for k in keys):
                found.append('拍摄位置（GPS）')
            model = keys.get('com.apple.quicktime.model') or keys.get('model')
            if model:
                found.append(f'手机型号（{model}）')
        if found:
            problems.append(f'`{f}` 带着{"、".join(found)}')
    return problems


if __name__ == '__main__':
    ps = main(sys.argv[1], sys.argv[2])
    for p in ps:
        print(' -', p)
    sys.exit(1 if ps else 0)
