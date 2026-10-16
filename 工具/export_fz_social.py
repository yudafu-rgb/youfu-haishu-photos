# -*- coding: utf-8 -*-
"""把福州攻略5篇导出成小红书/抖音发布包：每篇一个文件夹，编号图片（长边1440）+ 文案（含图片署名）。"""
import os, sys, shutil, importlib.util
from PIL import Image, ImageOps
REPO='/tmp/claude-0/s/repo'
spec=importlib.util.spec_from_file_location('fz',REPO+'/工具/build_fz.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SRC='/mnt/user-data/uploads/福州金鸡度假村/福州旅游五篇_高清图文攻略/images/'
OWNSRC={'beach':SRC+'beach.jpg','tea':SRC+'tea.jpg','house':SRC+'house.jpg'}
NAMES={16:'第16篇_福州48小时吃_高清版',17:'第17篇_福州3天2晚_高清版',18:'第18篇_福州8处低预算_高清版',19:'第19篇_福州周末山或海_高清版',20:'第20篇_福州2天慢游_高清版'}
dest=sys.argv[1]
def first_sentence(t):
    i=t.find('。')
    if i<0 or i>=len(t)-1: return t
    if t[:i+1].count('「')>t[:i+1].count('」'):
        j=t.find('」',i); return t if j<0 else t[:j+1]
    return t[:i+1]
def short(blocks):
    out=[]; first=True
    for b in blocks:
        k=b[0]
        if k=='img': continue
        if k=='h2': out.append('\n'+b[1])
        elif k=='h3': out.append('【'+b[1]+'】')
        elif k=='p': out.append(b[1] if first else first_sentence(b[1])); first=False
        elif k=='ul': out+=['· '+first_sentence(x) for x in b[1]]
        elif k=='table': out+=['· '+'｜'.join(r[:2]) for r in b[2]]
        elif k=='tip': out+=['· '+x for x in b[1][:2]]
        elif k=='stay': out.append('我们有福海墅就在龙鼓度假村里，门口就是沙滩，二楼茶室有免费的茉莉花茶。')
    return '\n'.join(out).strip()
for a in m.A:
    d=f'{dest}/{NAMES[a["no"]]}'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    imgs=m.images_of(a)[:9]
    files=[]; credits=[]
    for n,k in enumerate(imgs,1):
        src=OWNSRC.get(k, SRC+k+'.jpg')
        im=ImageOps.exif_transpose(Image.open(src)).convert('RGB'); im.thumbnail((1440,1440))
        fn=f'{n:02d}_{k}.jpg'; im.save(f'{d}/{fn}',quality=88,optimize=True); files.append(fn)
        ct=m.credit_text(k)
        if ct: credits.append(f'图{n}：{ct}')
    # 署名压缩：图号 作者（许可）
    parts=[]
    for n,k in enumerate(imgs,1):
        if k in m.OWN: continue
        c=m.CRED[k]; lic={'Public domain':'公有领域'}.get(c['license'],c['license'])
        parts.append(f'图{n} {c["artist"]}（{lic}）')
    cred='📷 网络照片来自 Wikimedia Commons：' + '、'.join(parts) + '。' if parts else ''
    body=short(a['body'])
    if len(body)+len(cred)+len(a['tags'])>990: print('TOO LONG',a['slug'],len(body)+len(cred)+len(a['tags']))
    xhs='\n'.join(['【标题】',a['xhs_title'],'','【正文】',body,'',cred,'','【话题】',a['tags'],'',
        '【图片顺序】（本文件夹里，按编号上传；01 是封面）']+files+['',
        '【注意】网络照片是 CC 许可，发布时正文末尾那行「图片来源」要保留。封面如果加字，加字后的图也要按同样的 CC BY-SA 许可、保留署名。',
        '','【官网同篇】'+f'{m.SITE}/fz/{a["slug"]}.html'])
    open(f'{d}/小红书文案.txt','w',encoding='utf-8-sig').write(xhs)
    hs=[b[1] for b in a['body'] if b[0]=='h2'][:6]
    dy='\n'.join([a['xhs_title'],'',a['body'][0][1],'']+['📍'+h for h in hs]+['',cred,'',a['tags'],'','【图片顺序】同小红书：'+'、'.join(files)])
    open(f'{d}/抖音图文文案.txt','w',encoding='utf-8-sig').write(dy)
    print(NAMES[a['no']], files)
