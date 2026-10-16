import subprocess, sys
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
R='/tmp/claude-0/s/repo/视频/客人体验/'
# 1) wave bed ~9s, filtered
run(['ffmpeg','-v','error','-y','-ss','1.0','-t','6.0','-i',R+'客人体验_沙滩踏浪.mp4','-ss','0','-t','3.1','-i',R+'客人体验_沙滩踏浪_2.mp4',
 '-filter_complex','[0:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1[a];[1:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1[b];[a][b]acrossfade=d=1.0,highpass=f=90,lowpass=f=2200,afftdn=nf=-30[o]',
 '-map','[o]','bed1.wav'])
# loop to 30s with crossfades
ins=[]
for _ in range(7): ins+=['-i','bed1.wav']
chain='[0][1]acrossfade=d=1.2[x1];'+''.join(f'[x{i}][{i+1}]acrossfade=d=1.2[x{i+1}];' for i in range(1,6))
run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',chain+'[x6]loudnorm=I=-30:TP=-6:LRA=7[o]','-map','[o]','bed.wav'])
def build(video, lines, total, out):
    inp=['-i',video,'-i','bed.wav']; fc=[]; labs=[]
    for i,(k,t0) in enumerate(lines):
        inp+=['-i',f'outn/{k}.wav']; idx=i+2
        ms=int((t0+0.6)*1000)
        fc.append(f'[{idx}:a]aresample=48000,adelay={ms}|{ms},apad[v{i}]')
        labs.append(f'[v{i}]')
    fc.append(''.join(labs)+f'amix=inputs={len(labs)}:normalize=0:duration=longest,atrim=0:{total},asplit[voice][key]')
    fc.append(f'[1:a]atrim=0:{total},afade=t=in:d=1,afade=t=out:st={total-1.5}:d=1.5[bedr]')
    fc.append('[bedr][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[ducked]')
    fc.append(f'[voice][ducked]amix=inputs=2:normalize=0,atrim=0:{total},afade=t=out:st={total-1.2}:d=1.2,alimiter=limit=0.89[aout]')
    run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map','0:v','-map','[aout]','-c:v','copy','-c:a','aac','-b:a','96k','-ac','2','-movflags','+faststart','-t',str(total),out])
D='/tmp/claude-0/s/repo/docs/video/'
build(D+'rooms.mp4',[('b1',0),('b2',5.4),('b3',9.8),('b4',13.2),('b5',18.6),('b6',23.0)],27.0,'rooms_av.mp4')
build(D+'seaside.mp4',[('a1',0),('a2',6.4),('a3',9.97),('a4',14.37),('a5',17.77),('a6',20.67)],25.67,'seaside_av.mp4')
print('ok')
