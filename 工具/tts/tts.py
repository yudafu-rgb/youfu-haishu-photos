import sherpa_onnx, soundfile as sf, sys, json
d='vits-melo-tts-zh_en/'
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=d+'model.onnx',lexicon=d+'lexicon.txt',tokens=d+'tokens.txt',dict_dir=d+'dict'),num_threads=4),rule_fsts=f'{d}date.fst,{d}number.fst,{d}phone.fst,{d}new_heteronym.fst',max_num_sentences=1)
tts=sherpa_onnx.OfflineTts(cfg)
lines=json.load(open(sys.argv[1]))
for k,t,sp in lines:
    a=tts.generate(t,sid=0,speed=sp)
    sf.write(f'out/{k}.wav',a.samples,a.sample_rate)
    print(k,round(len(a.samples)/a.sample_rate,2),t)
