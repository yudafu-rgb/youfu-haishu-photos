# -*- coding: utf-8 -*-
"""福州攻略栏目（第2版，基于「福州旅游五篇_高清图文攻略」）。
生成 docs/fz/*.html 和图片来源页；导出小红书 / 抖音文案到指定目录。
网上照片来自 Wikimedia Commons，署名与许可见 工具/fz_image_credits.json，网页上每张图下方都标注。
"""
import html, os, sys, json
REPO = '/tmp/claude-0/s/repo'
OUT = REPO + '/docs/fz'
SITE = 'https://youfuhaishu.com'
CSSV = '20261016c'
CRED = json.load(open(REPO + '/工具/fz_image_credits.json', encoding='utf-8'))
os.makedirs(OUT, exist_ok=True)

# 图片：key -> 网站路径（相对 docs/img/）
IMG = {k: f'fz/hd/{k}.jpg' for k in CRED if k not in ('beach', 'tea')}
IMG.update({'beach': 'hero.jpg', 'tea': 'g/g-tea.jpg', 'house': 'fz/hd/house.jpg'})
OWN = {'beach', 'tea', 'house'}  # 有福海墅自有照片，不标 CC 署名

STAY_NOTE = '有福海墅在琅岐岛龙鼓度假村里，门口就是沙滩，三栋海边别墅可以订单间，也可以整栋包下；二楼茶室有免费的茉莉花茶。'

A = [
dict(slug='food-48h', no=16, short='福州48小时吃什么',
 title='福州48小时吃什么：按片区吃，每顿少点一点', xhs_title='福州48小时吃什么｜先收藏，再给胃留点位置🍜',
 desc='福州两天怎么吃：按片区安排锅边、海蛎饼、捞化、芋泥、闽菜、牛滑、拌面扁肉和传统糕点，附交通和点单小抄，最后留一天去琅岐岛看海。',
 cover='guobian', tags='#福州美食 #福州48小时 #福州捞化 #福州小吃 #福州旅行 #琅岐岛',
 body=[
 ('p','来福州，收藏夹可以很满，第一顿不要太满。两天最舒服的吃法，是按片区走、每顿少点一点，把锅边、捞化、芋泥和闽菜慢慢排进去。'),
 ('img','guobian','锅边（鼎边糊）：一碗汤开场，别把早餐点成午宴'),
 ('h2','先选片区，别为一碗汤横穿全城'),
 ('table',['天数','片区','吃什么'],[['第一天','东街口、三坊七巷、达明路一带','锅边、海蛎饼、捞化、芋泥'],['第二天','台江、上下杭一带','牛滑、拌面扁肉、传统糕点、闽菜']]),
 ('p','去三坊七巷可以坐地铁到东街口站，上下杭一带查达道站附近的接驳。出口、营业时间和步行距离，以当天导航和店里公示为准。'),
 ('h2','第一天：早上一碗锅边，下午给芋泥留个位'),
 ('h3','早上：锅边配海蛎饼'),
 ('p','锅边也叫鼎边糊。先点一碗，海蛎饼和同行的人分一个。各家汤底和配料不一样，图里是一种做法。'),
 ('h3','中午：捞化'),
 ('p','捞化按配料算钱，先问清怎么计价再选。点单说「小份、配料少一点」，免得端上来一碗海鲜全家福。'),
 ('img','laohua','捞化（示意图，摄于北京的福州会馆）'),
 ('h3','下午：芋泥或花生汤，二选一'),
 ('p','芋泥适合两个人分着尝。甜度和配料各家不同，在意猪油、坚果的先问一句。'),
 ('img','yuni','芋泥'),
 ('h3','晚上：一顿闽菜收尾'),
 ('p','荔枝肉、爆炒双脆按人数点，不用每道都上。两个人先点一道主菜、一份青菜，不够再加。'),
 ('img','shuangcui','爆炒双脆'),
 ('h2','第二天：牛滑、拌面、糕点，按胃口做减法'),
 ('h3','早上：牛滑或拌面扁肉，选一样'),
 ('p','想喝热汤就选牛滑，想吃面就选拌面配扁肉。攻略列了两样，不代表要吃两顿早饭。'),
 ('img','niuhua','福州牛滑'),
 ('img','bianrou','拌面和扁肉'),
 ('h3','上午到午后：上下杭边逛边找糕点'),
 ('p','用「福州米时粿」「芋粿」这些关键词在地图上找附近的店，先看地址、营业时间和当天有没有货。'),
 ('h3','晚上：喜欢哪口，就再吃一次'),
 ('p','不一定要用一桌海鲜收尾。点海鲜先问清计价单位、重量、加工费和总价；想吃红鲟饭，先问有没有、什么规格、多少钱。'),
 ('tip',['地图搜「福州＋片区＋菜名」，确认不是外地同名店。','每顿只锁定一家主选、一家备选，排队太久就换。','问清食材、计价和分量。社区店、网红店都不等于便宜或好吃。']),
 ('h2','想续一个海边周末？另留一天给琅岐'),
 ('p','市区两天已经够吃，别再硬塞海岛往返。时间够的话再去琅岐岛，车程看当天导航。海边走一走，喝一杯茉莉花茶，吃饱以后，行程也留点白。'),
 ('img','tea','有福海墅二楼茶室'),
 ('stay', STAY_NOTE),
 ]),
dict(slug='3days-tips', no=17, short='福州3天2晚怎么排',
 title='福州3天2晚怎么排：老城、江边、看展各一天', xhs_title='福州3天2晚怎么排｜别把旅行排成早八课表',
 desc='第一次来福州 3 天怎么安排：三坊七巷和朱紫坊、烟台山和闽江边、福建博物院和西湖，每天留多久、怎么去，想加福道怎么替换。',
 cover='hearttree', tags='#福州旅游 #福州三日游 #三坊七巷 #烟台山 #福建博物院 #福州攻略',
 body=[
 ('p','第一次来福州，最容易高估的不是胃口，是每天能走多少路。三天按「老城、江边、看展」各一天来排，比把所有地名串成一条线好走得多。'),
 ('img','hearttree','三坊七巷的爱心榕树'),
 ('h2','3天路线总览'),
 ('table',['天数','主线','留多久（不含路上）'],[['第一天','三坊七巷 → 朱紫坊','前者 2–3 小时，后者约 1 小时'],['第二天','烟台山 → 仓前江边 / 闽江之心选一段','烟台山 2–3 小时，江边约 1 小时'],['第三天','福建博物院 → 西湖公园 → 返程','看展 2–3 小时，公园约 1 小时']]),
 ('h2','第一天：主街看热闹，侧巷慢慢走'),
 ('p','上午去三坊七巷，从东街口一带进老城。先认识南后街，再从郎官巷、黄巷、文儒坊里挑一两条走。拍照别堵住门口和通道；故居和展馆要不要买票，到了再看。'),
 ('img','sanfang','三坊七巷南后街夜景'),
 ('p','午饭就近解决，下午去朱紫坊看古厝和街巷，遇到喜欢的茶室再坐。晚上想去达明路就去，累了就早点休息。'),
 ('h2','第二天：烟台山和江边，留给一个慢下午'),
 ('p','烟台山可以从上藤站一带找接驳。坡道和台阶多，穿舒服的鞋。看完老建筑，再按体力去仓前江边或闽江之心的某一段。闽江之心很长，先选好具体去哪，别在两岸来回折返。'),
 ('img','yantaishan','烟台山公园月宫门'),
 ('img','zhongzhou','中洲岛和闽江夜景'),
 ('h2','第三天：看展加西湖，给返程留余量'),
 ('p','福建博物院和西湖公园挨着，先看展，再去湖边散步。返程早就缩短公园时间。'),
 ('img','museum','福建博物院'),
 ('p','福建省文旅厅的公开答复是参观福建博物院不用预约，特展和团队另看要求。一般周一闭馆，节假日以馆方公告为准；第三天碰上周一，就把三天顺序调一调。'),
 ('img','xihu','福州西湖'),
 ('h2','想加福道？用替换，不用叠加'),
 ('p','喜欢森林步道，就拿福道换掉第二天的一段，另留半天，先查好入口、走哪段和怎么回。'),
 ('img','fudao','福道森林步道'),
 ('h2','住哪里'),
 ('p','以市区为主，就按交通、行李和返程方向选。琅岐不在老城步行圈里，想去海边，另留半天到一天，或多住一晚，别每天往返赶市区景点。'),
 ('stay', STAY_NOTE + '适合一家人或几个朋友提前分好房，一起住。'),
 ]),
dict(slug='free-spots', no=18, short='福州8处低预算漫步地',
 title='福州8处低预算漫步地：门票省下来，买点芋泥', xhs_title='福州8处低预算漫步地｜门票省下来，买点芋泥✨',
 desc='福州不花门票也能逛：三坊七巷、上下杭、烟台山、福道、福建博物院、西湖公园、朱紫坊、闽江之心，每处留多久、和谁搭着走、哪些项目另收费。',
 cover='shangxiahang', tags='#福州免费景点 #福州低预算旅行 #福州Citywalk #福州慢游 #福州周边游',
 body=[
 ('p','好看的街巷、树荫和江风，不一定要先买联票。这 8 处都是公共空间，适合慢慢走；园里的展馆、商铺、游船和活动要不要钱，另外看。'),
 ('img','shangxiahang','上下杭'),
 ('h2','别一次走完：三组里挑一组'),
 ('ul',['老城组：三坊七巷＋朱紫坊，有兴趣再加一段西湖。','江边组：上下杭＋一段闽江之心，有体力再去烟台山。','看展或森林组：福建博物院＋西湖，或者福道单独半天。']),
 ('h2','1. 三坊七巷：逛街巷，不用进所有馆'),
 ('p','看古厝外观、马鞍墙和榕树，留 2–3 小时。爱心树顺路看，拍完让开通道；故居和专题展另看票务。'),
 ('h2','2. 上下杭：白天看建筑，晚上看街巷'),
 ('p','留 1.5–2 小时，看河道、会馆和老商埠。逛公共街巷不花钱，进馆、消费另算。'),
 ('img','shangxiahang_lane','上下杭的巷子'),
 ('h2','3. 烟台山：给坡道和休息都留时间'),
 ('p','留 2–3 小时，挑老建筑和江边的一小段走。可以从上藤站一带接驳。街区能逛，不代表每栋建筑都能进。'),
 ('img','yantaishan','烟台山公园'),
 ('h2','4. 福道：挑一段走，不用走完'),
 ('p','预留半天，含往返。出发前定好入口、出口，下雨天注意路滑。免费，但要提前看路线。'),
 ('img','fudao','福道'),
 ('h2','5. 福建博物院：看当期展览'),
 ('p','留 2–3 小时。官方口径是不用预约，特展和团队另看要求；一般周一闭馆。'),
 ('img','museum','福建博物院'),
 ('h2','6. 西湖公园：湖边坐一会儿，也算完成行程'),
 ('p','留 1–1.5 小时，可以和博物院连着走。游船这些项目另外收费。'),
 ('img','xihu','福州西湖'),
 ('h2','7. 朱紫坊：古厝街巷，别打扰居民'),
 ('p','留 1 小时左右，可以和三坊七巷放在同一天。走公共通道，想喝茶再进茶室。'),
 ('h2','8. 闽江之心：先选一个具体地方'),
 ('p','留 1 小时左右，按你在哪一岸挑一段走。想看中洲岛远景，先找好滨江的公共位置；灯光不是每天一样，游船另收费。'),
 ('img','zhongzhou','中洲岛夜景'),
 ('tip',['出发前查三件事：开放安排、当天交通、自己的体力。','省门票不等于要多走路，累了就坐。']),
 ('h2','想看海，就另留一天'),
 ('p','想延伸到琅岐岛，另留时间。海边散步不要门票，停车、租工具这些服务看现场。'),
 ('img','beach','琅岐岛龙鼓度假村门口的沙滩'),
 ('stay', STAY_NOTE),
 ]),
dict(slug='hidden-8', no=19, short='福州周末去哪：先选山还是海',
 title='福州周末去哪：8个方向，先选山还是海', xhs_title='福州周末去哪｜8个方向，先选山还是海',
 desc='福州周末备选：市区西禅寺、乌山，山里的鼓岭，海边的琅岐龙鼓，连江奇达村、永泰嵩口古镇、福清大姆山、马尾闽安古镇，按玩法和交通挑一个。',
 cover='guling', tags='#福州周边游 #琅岐岛 #福州海边 #福州自驾 #朋友聚会 #有福海墅',
 body=[
 ('p','周末最累的，有时是群里讨论三小时「到底去哪」。先选玩法，再选地方：下面是 8 个备选，不是一天能串完的路线。'),
 ('table',['方向','适合','建议时长','出发前查'],[['市区西禅寺','看古建、安静参访','半天','开放和参访规则'],['鼓岭','山间散步、老建筑','半天到一天','天气、上下山交通'],['琅岐龙鼓','海边散步、朋友度假','一天或两天一晚','潮汐、天气、住宿'],['连江奇达村','山海渔村、登高','一天','登高路线、山路交通'],['永泰嵩口古镇','古厝街巷、溪边慢逛','一天','往返交通'],['市区乌山','城市登高、散步','半天内','台阶、入口'],['福清大姆山','草场、山野','一天','景区公告、风雨'],['马尾闽安古镇','历史街巷、古桥','半天到一天','往返交通']]),
 ('h2','想留在市区：西禅寺、乌山二选一'),
 ('p','西禅寺适合愿意放慢脚步看古建的人，参访时保持安静；乌山适合只想加一段城市登高。带老人孩子，按台阶多少来选。'),
 ('img','xichan','福州西禅寺'),
 ('h2','想换换山里的空气：鼓岭'),
 ('p','天气好看山景，阴雨天就走一段路、看看老建筑。别为了「同款云海」追着天气跑，返程交通先确认。'),
 ('img','guling','鼓岭'),
 ('h2','想和朋友去海边：琅岐龙鼓沙滩'),
 ('p','这条适合单独留一天。上午或下午上岛，按当天潮汐决定要不要赶海，其他时间散步、喝茶、聚一聚。沙滩散步不等于适合游泳，低潮也不一定在傍晚。'),
 ('img','beach','琅岐岛龙鼓度假村门口的沙滩'),
 ('img','house','龙鼓度假村里的别墅'),
 ('p','出发前先定好日期、人数和房型，别等大家上了车才开始分床。天气变了，也可以把聚会挪到屋里。'),
 ('img','tea','有福海墅二楼茶室'),
 ('h2','想走远一点：连江、永泰、福清分开安排'),
 ('ul',['连江奇达村：山海和渔村，登高按开放情况和体力来，别为了拍照去危险的位置。','永泰嵩口古镇：看古厝和街巷，别和连江海边硬串成一天。','福清大姆山：山上风雨、道路会影响体验，看当天公告；草场上不生火、不留垃圾。','马尾闽安古镇：历史街巷方向的另一个选择。想和琅岐同一天去，先算好时间。']),
 ('h2','群里直接这样投票'),
 ('p','「想爬山的选鼓岭，想看古厝的选嵩口，想一起坐着聊天的选琅岐。」先定方向，再查天气、交通和开放情况，周末就没那么难定了。'),
 ('stay', STAY_NOTE + '天气不好时，楼里有茶室和麻将桌，几个人也有地方待。'),
 ]),
dict(slug='slow-2days', no=20, short='福州2天慢游',
 title='福州2天慢游：古巷、江风，累了就坐一会儿', xhs_title='福州2天慢游｜古巷、江风，累了就坐一会儿',
 desc='福州两天慢慢玩：第一天烟台山、闽菜和闽江边，第二天朱紫坊和上下杭；下雨换福建博物院；多一天就去琅岐岛海边。',
 cover='yantaishan', tags='#福州两日游 #福州慢游 #烟台山 #上下杭 #琅岐岛 #福州民宿',
 body=[
 ('p','两天不用把福州全装进行李箱。这条以市区为主，适合想慢慢走、喝茶、吃一顿闽菜的人；琅岐当作多一天的海边延伸，不硬塞进两天里。'),
 ('img','yantaishan','烟台山公园'),
 ('h2','路线一眼看懂'),
 ('table',['时间','去哪','怎么留白'],[['第一天下午','烟台山街巷和老建筑，2–3 小时','找个地方坐着歇会儿'],['第一天晚饭后','仓前江边或闽江之心一段，约 1 小时','不用两岸都走完'],['第二天上午','朱紫坊，约 1 小时','茶室、早餐按营业情况选'],['第二天午后','上下杭，1.5–2 小时','返程早就缩短，不补打卡']]),
 ('h2','第一天：烟台山和一段江风'),
 ('p','到了先放行李，再去烟台山。可以从上藤站一带找接驳。老建筑慢慢看，进室内先看开不开放；坡道走累了，就找个公共休息处坐会儿。下午就待在这一片，不再赶去三坊七巷。'),
 ('p','晚饭吃闽菜：荔枝肉、爆炒双脆按人数点，两个人先少点几道，想吃再加。'),
 ('img','shuangcui','爆炒双脆'),
 ('p','饭后去仓前江边，或者闽江之心挑一段走。想跨江先看步行条件和时间，别把一小时散步走成拉练。'),
 ('img','zhongzhou','中洲岛夜景'),
 ('h2','第二天：朱紫坊慢逛，再去上下杭'),
 ('p','上午留给朱紫坊，古厝和街巷慢慢看，这里有居民生活，别随便进不开放的院子。午后去上下杭看河道、古桥和会馆外观。'),
 ('img','shangxiahang','上下杭'),
 ('img','shangxiahang_lane','上下杭的巷子'),
 ('h2','下雨或不想多走'),
 ('p','把一段户外换成福建博物院，先看当天开放和当期展览，一般周一闭馆。'),
 ('img','museum','福建博物院'),
 ('h2','多一天：把时间留给琅岐海边'),
 ('p','市区玩完再去琅岐，车程看当天导航。看海、喝茶、和朋友聚聚；赶海看潮汐、天气和现场管理，赶不上低潮就安心散步。'),
 ('img','beach','琅岐岛龙鼓度假村门口的沙滩'),
 ('p','只有两天、又想住海边：第一天三坊七巷或烟台山二选一，下午去琅岐；第二天在海边歇一歇再返程，朱紫坊和上下杭留给下次。'),
 ('img','tea','有福海墅二楼茶室'),
 ('stay', STAY_NOTE + '14:00 以后入住，12:00 以前退房，住客停车免费。'),
 ]),
]

def esc(s): return html.escape(s, quote=True)

def credit_html(k):
    if k in OWN: return ''
    c = CRED[k]
    lic = f'<a href="{esc(c["licenseurl"])}" rel="license noopener" target="_blank">{esc(c["license"])}</a>' if c.get('licenseurl') else esc(c['license'])
    return f'<span class="credit">摄影：{esc(c["artist"])} · <a href="{esc(c["page"])}" rel="noopener" target="_blank">Wikimedia Commons</a> · {lic}</span>'

def credit_text(k):
    if k in OWN: return None
    c = CRED[k]; return f'{c["artist"]}（{c["license"]}，Wikimedia Commons）'

HEAD = '''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜有福海墅</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="../img/favicon-32.png">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
<link rel="stylesheet" href="../style.css?v=20261017c''' + CSSV + '''">
</head>
<body>
<header class="bar solid">
  <a class="brand" href="../" aria-label="有福海墅 首页"><img src="../img/logo.png" alt="">有福海墅</a>
  <nav aria-label="页面导航">
    <a href="../#rooms">房型</a>
    <a href="../guide/">琅岐攻略</a>
    <a href="./">福州攻略</a>
    <a href="../#book">预订</a>
  </nav>
</header>
'''
FOOT = '''<footer>
  <div class="wrap">
    <span>有福海墅 · 福州开发区金鸡度假有限公司 · <a href="{credits}">图片来源</a></span>
    <span>福建省福州市马尾区琅岐镇龙鼓度假村101号</span>
  </div>
</footer>
<details class="wx-float">
  <summary aria-label="微信咨询预订"><span>微信<br>咨询</span></summary>
  <div class="wx-float-pop">
    <img src="../img/wechat-qr.png" width="140" height="140" alt="有福海墅接待微信二维码" loading="lazy">
    <p>扫码问空房<br><a href="tel:13705088479">137 0508 8479</a></p>
  </div>
</details>
</body>
</html>
'''

def render(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p': out.append(f'<p>{esc(b[1])}</p>')
        elif k == 'h2': out.append(f'<h2>{esc(b[1])}</h2>')
        elif k == 'h3': out.append(f'<h3>{esc(b[1])}</h3>')
        elif k == 'img': out.append(f'<figure><img src="../img/{IMG[b[1]]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}{credit_html(b[1])}</figcaption></figure>')
        elif k == 'ul': out.append('<ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul>')
        elif k == 'table':
            th = ''.join(f'<th>{esc(h)}</th>' for h in b[1])
            rows = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in b[2])
            out.append(f'<div class="tbl"><table class="plan"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif k == 'tip': out.append('<div class="tip"><b>小贴士</b><ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul></div>')
        elif k == 'stay': out.append(f'<aside class="stay"><h2>住在海边</h2><p>{esc(b[1])}</p><div class="btns"><a class="btn solid" href="../#book">看怎么预订</a><a class="btn line" href="../#rooms">看看房间</a></div></aside>')
    return '\n'.join(out)

def build_site():
    for i, a in enumerate(A):
        url = f'{SITE}/fz/{a["slug"]}.html'; nxt = A[(i + 1) % len(A)]
        first_img = next((b[1] for b in a['body'] if b[0] == 'img'), None)
        cov = '' if first_img == a['cover'] and a['body'][1][0] == 'img' else f'<figure class="cover"><img src="../img/{IMG[a["cover"]]}" alt="{esc(a["short"])}"><figcaption>{credit_html(a["cover"])}</figcaption></figure>'
        page = HEAD.format(title=esc(a['title']), desc=esc(a['desc']), url=url, ogtype='article', img=f'{SITE}/img/{IMG[a["cover"]]}')
        page += f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">福州攻略</a></p>
    <h1>{esc(a['title'])}</h1>
    {cov}
{render(a['body'])}
    <p class="note">停留时长和路线是我们的建议，开放时间、票务、交通和店铺营业会变，出发前再查一下当天的信息。</p>
    <p class="next">下一篇：<a href="{nxt['slug']}.html">{esc(nxt['title'])}</a></p>
  </div>
</main>
''' + FOOT.format(credits='credits.html')
        open(f'{OUT}/{a["slug"]}.html', 'w').write(page)
    cards = '\n'.join(f'''    <a class="gcard" href="{a['slug']}.html">
      <img src="../img/{IMG[a['cover']]}" alt="{esc(a['short'])}" loading="lazy">
      <h2>{esc(a['short'])}</h2>
      <p>{esc(a['desc'])}</p>
    </a>''' for a in A)
    idx = HEAD.format(title='福州吃喝玩乐攻略', desc='福州怎么吃、怎么逛：48小时美食、3天2晚路线、8处低预算漫步地、周末山海方向、2天慢游，最后留一天去琅岐岛看海。', url=f'{SITE}/fz/', ogtype='website', img=f'{SITE}/img/{IMG["guobian"]}')
    idx += f'''<main class="article">
  <div class="wrap">
    <p class="crumb"><a href="../">首页</a> / 福州攻略</p>
    <h1>福州吃喝玩乐攻略</h1>
    <p class="lead">来琅岐岛之前，先在福州市区吃一圈、逛一圈。这是我们给客人整理的路线和吃法；岛上怎么玩，看<a href="../guide/">琅岐岛攻略</a>。</p>
    <div class="gcards">
{cards}
    </div>
  </div>
</main>
''' + FOOT.format(credits='credits.html')
    open(f'{OUT}/index.html', 'w').write(idx)
    # 图片来源页
    used = []
    for a in A:
        for b in a['body']:
            if b[0] == 'img' and b[1] not in used and b[1] not in OWN: used.append(b[1])
        if a['cover'] not in used and a['cover'] not in OWN: used.append(a['cover'])
    rows = ''.join(f'<li><img src="../img/{IMG[k]}" alt="" loading="lazy"><div><b>{esc(CRED[k]["title"].replace("File:",""))}</b><br>摄影：{esc(CRED[k]["artist"])}<br>许可：<a href="{esc(CRED[k]["licenseurl"])}" rel="license">{esc(CRED[k]["license"])}</a> · <a href="{esc(CRED[k]["page"])}">原始文件页</a><br>网页上按比例缩小显示，未做其他修改。</div></li>' for k in used)
    cp = HEAD.format(title='福州攻略图片来源', desc='福州攻略栏目所用网络照片的作者、来源和许可。', url=f'{SITE}/fz/credits.html', ogtype='website', img=f'{SITE}/img/hero.jpg')
    cp += f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">福州攻略</a> / 图片来源</p>
    <h1>图片来源</h1>
    <p>福州攻略里的景点和菜品照片来自 Wikimedia Commons，按各自的许可使用并署名。照片作者与有福海墅没有合作关系，照片也不代表作者推荐。海滩、茶室、别墅照片是有福海墅自己拍的。</p>
    <ul class="credits">{rows}</ul>
  </div>
</main>
''' + FOOT.format(credits='credits.html')
    open(f'{OUT}/credits.html', 'w').write(cp)

def plain(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'img': continue
        if k == 'h2': out.append('\n' + b[1])
        elif k == 'h3': out.append('【' + b[1] + '】')
        elif k == 'p': out.append(b[1])
        elif k == 'ul': out += ['· ' + x for x in b[1]]
        elif k == 'table': out += ['· ' + '｜'.join(r) for r in b[2]]
        elif k == 'tip': out += ['小贴士：'] + [f'{n}. {x}' for n, x in enumerate(b[1], 1)]
        elif k == 'stay': out.append(b[1])
    return '\n'.join(out).strip()

def images_of(a):
    seen = [a['cover']]
    for b in a['body']:
        if b[0] == 'img' and b[1] not in seen: seen.append(b[1])
    return seen

if __name__ == '__main__':
    build_site()
    print('ok')
