# -*- coding: utf-8 -*-
import subprocess, os, sys
R = '/tmp/claude-0/s/repo/视频/'
W = '/tmp/claude-0/-home-claude/d5d9bfe0-b383-59bb-bc15-ab8c3ff63a18/scratchpad/vbuild/'
os.makedirs(W, exist_ok=True)
FONT = 'Noto Serif CJK SC SemiBold'
XF = 0.6  # crossfade seconds

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2000:]); sys.exit(1)

def seg(name, src, start, dur, size, crop=None, speed=1.2, cap=None, title=None, ty=0.40, grade='eq=contrast=1.05:saturation=1.12:brightness=0.02'):
    """Cut [start,start+dur] of source time, stabilise, grade, fit to size, add caption. Output length = dur/speed."""
    w, h = size
    raw = W + name + '_raw.mp4'
    vf0 = 'setpts=PTS-STARTPTS'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', R + src, '-an', '-vf', vf0, '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', raw])
    trf = W + name + '.trf'
    run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-vf', f'vidstabdetect=shakiness=6:accuracy=12:result={trf}', '-f', 'null', '-'])
    f = [f'vidstabtransform=input={trf}:smoothing=24:zoom=4:optzoom=0', 'unsharp=5:5:0.5']
    if crop: f.append(crop)
    f += [f'scale={w}:{h}:force_original_aspect_ratio=increase', f'crop={w}:{h}', grade, f'setpts=PTS/{speed}', 'fps=30']
    out_len = dur / speed
    if title:
        t1, t2 = title
        f = [x for x in f]

        f.append(f"drawtext=font='{FONT}':text='{t1}':fontsize={int(w*0.085)}:fontcolor=white:x=(w-text_w)/2:y=h*{ty}:shadowcolor=black@0.45:shadowx=0:shadowy=2:borderw=2:bordercolor=black@0.3:alpha='if(lt(t,0.4),t/0.4,if(gt(t,{out_len-0.8}),max(0,({out_len}-t)/0.8),1))'")
        f.append(f"drawtext=font='{FONT}':text='{t2}':fontsize={int(w*0.04)}:fontcolor=white:x=(w-text_w)/2:y=h*{ty}+{int(w*0.12)}:shadowcolor=black@0.45:shadowx=0:shadowy=2:borderw=2:bordercolor=black@0.3:alpha='if(lt(t,0.7),max(0,(t-0.3)/0.4),if(gt(t,{out_len-0.8}),max(0,({out_len}-t)/0.8),1))'")
    if cap:
        fs = int(min(w, h) * 0.066)
        f.append(f"drawtext=font='{FONT}':text='{cap}':fontsize={fs}:fontcolor=white:x={int(fs*1.1)}:y=h-{int(fs*2.6)}:shadowcolor=black@0.5:shadowx=0:shadowy=2:borderw=2:bordercolor=black@0.35:alpha='if(lt(t,0.5),0,if(lt(t,1.0),(t-0.5)/0.5,if(gt(t,{out_len-0.7}),max(0,({out_len}-t)/0.7),1)))'")
    out = W + name + '.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-vf', ','.join(f), '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', out])
    return out, out_len

def join(parts, out, size, crf=27):
    inputs = []
    for p, _ in parts: inputs += ['-i', p]
    fc = []; prev = '[0:v]'; t = parts[0][1]
    for i in range(1, len(parts)):
        lab = f'[v{i}]'
        fc.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={t - XF:.3f}{lab}')
        prev = lab; t = t - XF + parts[i][1]
    fc.append(f'{prev}fade=t=in:st=0:d=0.6,fade=t=out:st={t-0.8:.3f}:d=0.8,format=yuv420p[out]')
    run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]', '-an', '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-profile:v', 'high', '-movflags', '+faststart', out])
    print(out, round(t, 1), 's', os.path.getsize(out) // 1024, 'KB')

V = (720, 1280)
which = sys.argv[1] if len(sys.argv) > 1 else 'ab'
if 'a' in which:
    A = [
        seg('a1', '园区/园区_度假村环境.mp4', 35, 8.4, V, title=('有福海墅', '福州 · 琅岐岛 · 龙鼓度假村'), ty=0.12),
        seg('a2', '客人体验/客人体验_海边打牌.mp4', 42, 5.0, V, cap='穿过防风林'),
        seg('a3', '客人体验/客人体验_海边打牌.mp4', 30, 6.0, V, cap='出门就是海'),
        seg('a4', '周边/周边_光影沙滩漫步_1.mp4', 9.5, 4.8, V, crop='crop=iw:ih*0.82:0:0', cap='退潮后的大沙滩'),
        seg('a5', '周边/周边_光影沙滩漫步_1.mp4', 3.2, 4.2, V, crop='crop=iw:ih*0.85:0:0', cap='远处是白猴礁'),
        seg('a6', '活动/活动_打铁花表演.mp4', 17.5, 5.0, V, crop='crop=ih*0.5625:ih:(iw-ih*0.5625)/2:0', speed=1.0, cap='夜里看打铁花', grade='eq=contrast=1.08:brightness=-0.10:gamma=0.80:saturation=0.85'),
    ]
    join(A, W + 'seaside.mp4', V, crf=30)
if 'b' in which:
    H = (1280, 720)
    B = [
        seg('b1', '房间实拍/红花阁_内部实拍_1.mp4', 2, 7.2, H, title=('别墅里面', '六栋别墅 · 每栋五间房')),
        seg('b2', '房间实拍/红花阁_内部实拍_1.mp4', 22, 6.0, H, cap='一楼客厅、餐桌、牌桌、麻将桌'),
        seg('b3', '房间实拍/兰楼菊花阁_202_实拍.mp4', 0, 4.8, H, cap='二楼榻榻米、茶桌'),
        seg('b4', '房间实拍/白阁_101_实拍.mp4', 17.5, 7.2, H, cap='双床房 · 一家四口正好'),
        seg('b5', '房间实拍/白阁_202_实拍.mp4', 17.5, 6.0, H, cap='每间房都有空调和独立卫浴'),
        seg('b6', '房间实拍/白阁_101_实拍.mp4', 26.5, 4.8, H, cap='推开窗就是绿树'),
    ]
    join(B, W + 'rooms.mp4', H, crf=28)
