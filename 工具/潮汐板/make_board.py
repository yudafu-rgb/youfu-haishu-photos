"""生成有福海墅电子潮汐板。用法: python3 make_board.py 2026-10-07 [输出目录]
数据: tides.json（来源 eisk.cn 闽江口(川石岛) 站，国家海洋信息中心天文潮预报）"""
import json,sys,os,datetime,glob
from PIL import Image,ImageDraw,ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=lambda p,s: ImageFont.truetype(p,s,index=2)
HERE=os.path.dirname(os.path.abspath(__file__))
LOGO=(glob.glob('/home/claude/youfu-haishu-photos/Logo/*.png')+[None])[0]
def m(t): h,mi=map(int,t.split(':')); return h*60+mi
def hm(x): x=max(0,min(x,24*60-1)); return f'{x//60:02d}:{x%60:02d}'
def best(day):
    sr,ss=m(day['sun'][0]),m(day['sun'][1]); out=[]
    for t,k,_ in day['ev']:
        if k!='L': continue
        a,b=max(m(t)-120,sr+15),min(m(t)+120,ss)
        if b-a>=60: out.append((a,b))
    return out
def pick(day,kind):
    am=[e for e in day['ev'] if e[1]==kind and m(e[0])<12*60]; pm=[e for e in day['ev'] if e[1]==kind and m(e[0])>=12*60]
    f=lambda L: L[0][0] if L else '—'
    return f(am),f(pm)
def draw(date,day,out):
    W,H=1080,1800; BG=(250,247,240); INK=(30,58,82); ACC=(214,110,72); SUB=(105,115,125)
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,300],fill=INK)
    d.text((70,55),'今日潮汐',font=F(B,110),fill='white')
    d.text((74,200),'有福海墅 · 琅岐岛龙鼓沙滩',font=F(R,40),fill=(220,232,240))
    if LOGO:
        L=Image.open(LOGO).convert('RGBA'); bb=L.getbbox(); L=L.crop(bb); L.thumbnail((180,180))
        pl=Image.new('RGB',(210,210),'white'); pl.paste(L,((210-L.width)//2,(210-L.height)//2),L); im.paste(pl,(W-270,45))
    dt=datetime.date.fromisoformat(date); wk='一二三四五六日'[dt.weekday()]
    y=350
    d.text((70,y),f'{dt.month}月{dt.day}日  星期{wk}',font=F(B,64),fill=INK)
    lu=day.get('lunar','').split('(')[0].split(); d.text((72,y+90),'农历'+' · '.join(lu),font=F(R,36),fill=SUB)
    y+=190; d.line([70,y,W-70,y],fill=(214,205,190),width=3); y+=40
    for lab,kind in [('退潮最低','L'),('涨潮最高','H')]:
        a,p=pick(day,kind)
        d.text((70,y),lab,font=F(B,54),fill=INK)
        d.text((400,y+6),'上午',font=F(R,40),fill=SUB); d.text((500,y-4),a,font=F(B,60),fill=INK)
        d.text((730,y+6),'下午',font=F(R,40),fill=SUB); d.text((830,y-4),p,font=F(B,60),fill=INK)
        y+=120
    y+=20; bs=best(day)
    d.rounded_rectangle([50,y,W-50,y+330],radius=36,outline=ACC,width=6,fill=(253,236,226))
    d.text((95,y+35),'今天最适合赶海、沙滩写字',font=F(B,54),fill=ACC)
    if bs:
        txt='   '.join(f'{hm(a)} ～ {hm(b)}' for a,b in bs[:2])
        d.text((95,y+130),txt,font=F(B,78 if len(bs)==1 else 56),fill=INK)
        d.text((95,y+250),'退潮前后约 2 小时，沙滩最大、最平',font=F(R,34),fill=SUB)
    else:
        d.text((95,y+130),'今天白天潮水不合适',font=F(B,64),fill=INK)
        d.text((95,y+250),'推荐上天台看海、喝茶、吹海风',font=F(R,34),fill=SUB)
    y+=390
    d.text((70,y),'今日日落',font=F(B,54),fill=INK); d.text((400,y-4),'约 '+day['sun'][1],font=F(B,60),fill=INK); d.text((690,y+8),'去天台或沙滩看',font=F(R,38),fill=SUB)
    y+=130
    d.text((70,y),'温馨提醒',font=F(B,44),fill=INK); yy=y+75
    for t in ['涨潮时请离开礁石和远处滩涂，看好孩子','礁石湿滑，请穿防滑鞋','挖沙工具可在前台借用，用完请放回','小螃蟹、小贝壳拍完照放回大海，垃圾带走']:
        d.text((80,yy),'·  '+t,font=F(R,36),fill=SUB); yy+=60
    d.text((70,H-60),'数据：国家海洋信息中心天文潮预报（闽江口站），实际以现场为准',font=F(R,26),fill=(160,165,170))
    os.makedirs(out,exist_ok=True); p=os.path.join(out,f'潮汐板_{date}.png'); im.save(p); return p
if __name__=='__main__':
    date=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else '.'
    T=json.load(open(os.path.join(HERE,'tides.json'),encoding='utf-8'))
    if date not in T or not T[date]['ev']: sys.exit(f'没有 {date} 的潮汐数据，先更新 tides.json')
    print(draw(date,T[date],out))
