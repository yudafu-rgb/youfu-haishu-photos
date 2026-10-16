# -*- coding: utf-8 -*-
"""福州攻略栏目：生成 docs/fz/*.html，并导出小红书/抖音文案。
图片：福州市区的图放 docs/img/fz/<文件名>（来自用户提供的 images 文件夹）；文件不存在时自动跳过该图。
"""
import html, os, sys, datetime
REPO = '/tmp/claude-0/s/repo'
OUT = REPO + '/docs/fz'
SITE = 'https://youfuhaishu.com'
CSSV = '20261016'
os.makedirs(OUT, exist_ok=True)

def has(img):
    return os.path.exists(f'{REPO}/docs/img/{img}')

# blocks: ('p',text) ('h2',text) ('h3',text) ('img',path_under_img,alt) ('ul',[..]) ('ol',[..]) ('tip',[..]) ('stay',text)
A = [
dict(slug='food-48h', no=16,
 title='福州48小时吃什么：一条只为吃的路线', xhs_title='福州48小时纯吃路线｜吃货直接收藏🍜',
 desc='来福州两天怎么吃：锅边糊、海蛎饼、捞化、芋泥、花生汤、荔枝肉、红鲟饭、牛滑、煎包，按早中晚排好的吃货路线，最后去琅岐岛加一顿海鲜。',
 cover='fz/guobianhu.jpg', cover_alt='锅边糊和海蛎饼', fallback='g/g-crab.jpg',
 tags='#福州美食 #福州48小时 #福州捞化 #闽菜 #福州小吃 #有福之州 #琅岐岛',
 body=[
 ('p','来福州，主线任务就是吃。这条路线不硬塞景点，从早餐吃到夜宵：锅边糊、捞化、芋泥、红鲟饭，跟着本地口味走就行。'),
 ('p','下面提到的都是本地人常说的老店。小店营业时间常有变化，出发前在地图上再查一下。'),
 ('h2','第一天：老福州的经典味道'),
 ('h3','早餐：锅边糊配海蛎饼'),
 ('p','随便找一家老社区早餐店就有。锅边糊鲜香顺口，海蛎饼外酥里嫩，两样一起吃，就是福州早餐的标准答案。'),
 ('img','fz/guobianhu.jpg','一碗锅边糊'),
 ('h3','上午：先锋市场'),
 ('p','喜欢软糯口感的会逛得很开心：芋泥、马蹄糕、藕糕、花生汤都找得到。每样少买一点，给后面的正餐留胃。'),
 ('h3','午餐：现挑海鲜'),
 ('p','在海鲜市场现挑膏蟹、生蚝、活虾，看当天有什么。做法越简单，越吃得出鲜。'),
 ('h3','下午：忠惠酱鸭捞化'),
 ('p','酱鸭是灵魂，卤香渗进粉干里，再蘸一点蒜头酱，咸香开胃。'),
 ('img','fz/jiangyalao.jpg','酱鸭捞化'),
 ('h3','甜品：没牙伯花生汤、芋泥'),
 ('p','花生炖得软糯，芋泥绵密，芝麻香一上来，就是很典型的福州甜口。'),
 ('img','fz/huashengtang.jpg','一碗花生汤'),
 ('h3','晚餐：闽菜馆（如紫阳海鲜楼）'),
 ('p','想集中尝闽菜，点荔枝肉、红鲟饭、爆炒双脆。人多更合适，多点几样一起分。'),
 ('img','fz/lizhirou.jpg','荔枝肉'),
 ('img','fz/hongxunfan.jpg','红鲟饭'),
 ('h2','第二天：牛滑、煎包和古早糕点'),
 ('h3','早餐：依强牛肉店'),
 ('p','牛滑汤配小笼包，汤头鲜甜，早上吃很舒服。'),
 ('h3','午餐：煎包配鱼丸汤'),
 ('p','煎包皮薄、底脆、肉馅多汁，再配一碗鱼丸汤。轮工壹号是常被提到的一家。'),
 ('h3','午后：古早糕点'),
 ('p','马蹄糕、清明粿这些闽式糕点，在彬德桥米时粿这类老店每样买一点，慢慢尝。'),
 ('h3','傍晚：达明路边走边吃'),
 ('p','甘草芭乐、芋泥饼挑喜欢的买，不用每家都打卡，留一点给下次。'),
 ('tip',['福州口味偏甜鲜，不习惯甜口的，点单前问一句。','别只盯着景区主街，老社区小店更有日常味道。','几个人一起最划算：每样少点一点，分着吃，能尝得更多。','店铺营业时间和菜品会变，出发前再确认。']),
 ('h2','再加一顿：去琅岐岛吃海鲜'),
 ('p','市区吃完一轮，想换个环境，开车约 40 分钟到琅岐岛。去码头挑当天的海鲜，再到海边散步吹风，节奏一下就慢下来了。'),
 ('img','g/g-crab.jpg','琅岐岛码头刚买的螃蟹'),
 ('stay','我们有福海墅就在琅岐岛龙鼓度假村里，门口就是沙滩。整栋别墅适合朋友小聚、公司团建，天台烧烤架免费用（食材、炭自带），二楼茶室可以泡茉莉花茶聊天。'),
 ]),
dict(slug='3days-tips', no=17,
 title='第一次来福州玩3天：路线和5条实用建议', xhs_title='第一次来福州玩3天｜这5条建议能少走弯路‼️',
 desc='第一次来福州 3 天怎么安排：三坊七巷、朱紫坊、上下杭、烟台山、闽江之心、福道、西禅寺、福建博物院的路线，以及逛巷子、走福道、看夜景和预约的建议。',
 cover='fz/zhongzhoudao.jpg', cover_alt='闽江上的中洲岛', fallback='g/g-bridge.jpg',
 tags='#福州旅游 #福州攻略 #福州旅行建议 #三坊七巷 #烟台山 #闽江之心 #琅岐岛 #有福之州',
 body=[
 ('p','我们在琅岐岛开民宿，第一次来福州的客人常问：市区几天怎么排？整理了一条 3 天路线和 5 条建议，不赶路，少走冤枉路。'),
 ('h2','3天怎么走'),
 ('ul',['第一天：三坊七巷 → 朱紫坊 → 上下杭 → 中洲岛夜景','第二天：烟台山 → 闽江之心 → 福道','第三天：西禅古寺 → 福建博物院 → 返程']),
 ('h2','5条建议'),
 ('h3','1. 三坊七巷别只逛南后街'),
 ('p','主街热闹，适合慢慢看的是郎官巷、黄巷、文儒坊这些侧巷。想拍爱心树就错开人多的时候。鱼丸、肉燕不必在主街解决，往周边老社区走走，选择更多。'),
 ('img','fz/sanfang.jpg','三坊七巷'),
 ('h3','2. 福道按体力选入口'),
 ('p','福道入口很多，想省力就提前在地图上看好进出口，少爬坡。傍晚去最舒服，光线也好。出入口开放情况以现场公示为准。'),
 ('h3','3. 烟台山傍晚去'),
 ('p','夕阳落在红砖老洋房上，比正午更有味道。石厝教堂、爱国路一带顺路走，不用来回折返。'),
 ('h3','4. 中洲岛适合远看'),
 ('p','从闽江两岸看中洲岛的蓝调夜景最好看。专程进岛的话，先了解一下岛上开放情况。'),
 ('img','fz/zhongzhoudao.jpg','闽江上的中洲岛'),
 ('h3','5. 福建博物院提前查预约'),
 ('p','出发前查一下官方开放时间和预约要求，避免跑空。'),
 ('h2','吃住怎么选'),
 ('ul',['吃：网红街可以逛，不必每家排队。捞化、肉燕、锅边糊、芋泥，在老社区更容易吃到日常口味。','住：第一次来，东街口、达明路附近交通和夜宵都方便。','想放空：市区逛完，再留一天去琅岐岛，海边散步、看潮汐，在茶室坐一下午。']),
 ('p','福州不适合特种兵式打卡。巷子里慢慢走，江边吹吹风，才更接近这座城的味道。'),
 ('img','hero.jpg','琅岐岛龙鼓度假村门口的沙滩'),
 ('stay','最后一天想看海，可以住到琅岐岛的有福海墅：门口就是沙滩，整栋别墅适合朋友聚会、团队活动，楼里有茶室和麻将桌。'),
 ]),
dict(slug='free-spots', no=18,
 title='福州慢游清单：这些地方大多免费', xhs_title='福州慢游清单｜这些宝藏地方大多免费✨',
 desc='福州低预算怎么玩：三坊七巷、上下杭、烟台山、福道、福建博物院、西湖公园、朱紫坊、闽江之心，大多不要门票；再留一天去琅岐岛看海。',
 cover='fz/sanfang.jpg', cover_alt='三坊七巷古厝', fallback='g/g-bay.jpg',
 tags='#福州免费景点 #福州慢游 #福州citywalk #有福之州 #福州旅行 #琅岐岛 #福州周边游',
 body=[
 ('p','预算有限也能好好逛福州。老城街巷、森林步道、城市园林和博物馆，串起来就是一条很有榕城味道的低预算路线。门票和开放规则会变，出发前再查一下。'),
 ('h2','三坊七巷：街巷免费'),
 ('p','看马鞍墙古厝、找爱心榕树，重点是钻进侧巷慢慢走。部分名人故居和展馆单独收费，只逛街巷不要门票。'),
 ('img','fz/sanfang.jpg','三坊七巷的古厝和榕树'),
 ('h2','上下杭：晚上更有味道'),
 ('p','沿河看老会馆、古民居和商埠遗迹。灯笼亮起来以后很好看，节奏也比热门景点松。'),
 ('h2','烟台山：老洋房和闽江落日'),
 ('p','红砖洋房、石厝教堂、闽江观景位都在步行范围内。傍晚到，顺着夕阳一路逛到亮灯。'),
 ('h2','福道：傍晚走进森林'),
 ('p','空中森林步道，适合散步看绿意。想少爬坡，先看好进出口再走。'),
 ('h2','福建博物院：注意预约和闭馆'),
 ('p','想系统了解闽越历史，安排在午后很合适。提前查官方开放时间和预约要求。'),
 ('h2','西湖公园：本地人散步的地方'),
 ('p','湖景、古榕树、开化寺都在一片园林里，不追机位也逛得很舒服。'),
 ('img','fz/xihu.jpg','西湖公园的大榕树'),
 ('h2','朱紫坊：安静版老城'),
 ('p','古巷、小桥和茶室藏在街区里，人少的时候特别适合慢走。离三坊七巷不远，可以放在同一天。'),
 ('h2','闽江之心：一段免费的江风'),
 ('p','晚上沿江散步，看解放大桥的灯光和中洲岛远景，留一个小时吹风就够。'),
 ('h2','再多留一天：去琅岐岛看海'),
 ('p','市区的免费景点逛得差不多了，可以把行程延到琅岐岛。沙滩散步、赶海不要门票，赶海要看潮汐、天气和现场安全提示。'),
 ('img','g/g-boardwalk.jpg','琅岐岛防风林里的木栈道'),
 ('stay','有福海墅在琅岐岛龙鼓度假村里，门口就是沙滩，二楼茶室可以免费尝茉莉花茶，适合把一天收在海风和一壶茶里。'),
 ]),
dict(slug='hidden-8', no=19,
 title='福州不只有三坊七巷：8个小众好去处', xhs_title='福州不只有三坊七巷｜8个小众宝藏地',
 desc='福州小众景点：西禅古寺、鼓岭、琅岐龙鼓海滩、连江奇达村、永泰嵩口古镇、乌山、红坊、福清大姆山草场，古寺、山林、海滩、渔村、草场各有风景。',
 cover='fz/haitan.jpg', cover_alt='琅岐龙鼓海滩', fallback='hero.jpg',
 tags='#福州小众景点 #琅岐岛 #福州海边 #福州周边游 #福州自驾 #有福海墅',
 body=[
 ('p','来福州别把行程全塞在老城。古寺、山林、海滩、渔村、草场，风景完全不一样，挑两三个慢慢走就好。开放时间和收费以现场公示为准。'),
 ('h2','1. 西禅古寺'),
 ('p','千年古寺、古荔枝树、红墙古塔，整体安静，很有禅意。'),
 ('h2','2. 鼓岭'),
 ('p','百年避暑老别墅散在山间，遇上云雾天很有层次。适合周末短途自驾，留半天慢慢走。'),
 ('h2','3. 龙鼓海滩（琅岐金鸡报晓海滩）'),
 ('p','从福州市区开车约 40 分钟。沙滩、防风林和海风，很适合几个人短途度假。按潮汐安排赶海，日落要看天气和一点运气。'),
 ('img','fz/haitan.jpg','琅岐龙鼓海滩'),
 ('img','g/g-boardwalk.jpg','海滩边防风林里的木栈道'),
 ('h2','4. 奇达村（连江）'),
 ('p','山海渔村，岩壁、海湾和村落同框。想拍高处的全景要预留爬山时间，穿适合走山路的鞋。'),
 ('h2','5. 嵩口古镇（永泰）'),
 ('p','保留了夯土黄墙和传统古厝，商业气息相对淡，适合喜欢老建筑和安静街巷的人。'),
 ('h2','6. 乌山'),
 ('p','市中心就能到的山林公园，福州「三山两塔」之一。免费、好走，还能俯瞰老城。'),
 ('h2','7. 红坊'),
 ('p','红砖老厂房、藤蔓墙和文艺空间集中在一起，适合半天轻逛。园区业态会调整，出发前确认开放情况。'),
 ('h2','8. 大姆山草场（福清）'),
 ('p','大片草甸和起伏山野，适合野餐、拍照。山上天气变化快，提前看天气，注意防晒、防风、带水。'),
 ('h2','周末怎么排'),
 ('p','想轻松一点，可以把龙鼓海滩单独排成一两天：白天看海、赶海，傍晚去码头挑海鲜。'),
 ('img','g/g-dusk.jpg','傍晚的龙鼓度假村'),
 ('stay','有福海墅就在龙鼓度假村里，门口就是沙滩。整栋别墅适合朋友聚会、家庭出游、公司团建，楼里有茶室和麻将桌，天气不好也有地方待。'),
 ]),
dict(slug='slow-2days', no=20,
 title='福州2日慢游：不赶路的玩法', xhs_title='福州2日松弛路线｜不赶路才是正确打开方式',
 desc='福州两天慢慢玩：烟台山老洋房和闽江日落、社区闽菜馆、闽江之心夜景、朱紫坊喝茶、上下杭；还有一天就去琅岐岛海边。',
 cover='fz/yantaishan.jpg', cover_alt='烟台山石厝教堂', fallback='roof.jpg',
 tags='#福州松弛旅行 #福州两日游 #福州慢生活 #福州闺蜜游 #琅岐岛 #有福海墅',
 body=[
 ('p','不想特种兵式打卡，就试试这条两天的路线：每一站都留时间坐下来，适合闺蜜、情侣或一个人慢慢逛。'),
 ('h2','第一天：老洋房、闽菜和江边夜景'),
 ('h3','下午：烟台山'),
 ('p','先去烟台山。红砖老洋房、石厝教堂和街角小店都适合慢慢走，不用赶固定机位。'),
 ('img','fz/yantaishan.jpg','烟台山石厝教堂'),
 ('h3','傍晚：等一场闽江日落'),
 ('p','夕阳落在老建筑上，颜色比正午柔和很多。找个视野舒服的位置停下来，比拍完就走更让人记得住。'),
 ('h3','晚餐：社区闽菜馆'),
 ('p','点一份荔枝肉，再配糟小肠或当天的时令菜。两个人不用点太多，慢慢吃。'),
 ('h3','夜里：闽江之心'),
 ('p','饭后沿江散步，看解放大桥的灯光和中洲岛夜景，江风一吹，一天的累就散了。'),
 ('h2','第二天：古巷、茶室和老商埠'),
 ('h3','上午：朱紫坊'),
 ('p','早点去，人少巷子静。沿着古厝慢慢走，遇到喜欢的茶室就坐下来喝一壶。'),
 ('h3','午后：上下杭'),
 ('p','沿河看会馆、商埠老宅和古桥。累了就歇，这条路线本来就不赶。'),
 ('h2','还有一天：去海边'),
 ('p','想彻底躲开人潮，再留一天去琅岐岛：海边吹风、看潮汐，在防风林下坐一会儿。赶海和户外活动以潮汐、天气和现场安全提示为准。'),
 ('img','g/g-tea.jpg','有福海墅二楼茶室'),
 ('stay','有福海墅门口就是沙滩，二楼茶室有免费的茉莉花茶，几个人还能在楼下打牌、喝茶，适合朋友小聚。'),
 ('p','福州旅行的重点，不是打卡所有地标，而是慢慢过几天闽式生活：古厝里喝茶，江边吹风，海边等一场日落。'),
 ]),
]

def esc(s): return html.escape(s, quote=True)
def imgok(b): return b[0] != 'img' or has(b[1])

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
<link rel="stylesheet" href="../style.css?v=''' + CSSV + '''">
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
    <span>有福海墅 · 福州开发区金鸡度假有限公司</span>
    <span>福建省福州市马尾区琅岐镇龙鼓度假村101号</span>
  </div>
</footer>
</body>
</html>
'''

def cover_of(a):
    return a['cover'] if has(a['cover']) else a['fallback']

def render(blocks):
    out = []
    for b in blocks:
        if not imgok(b): continue
        k = b[0]
        if k == 'p': out.append(f'<p>{esc(b[1])}</p>')
        elif k == 'h2': out.append(f'<h2>{esc(b[1])}</h2>')
        elif k == 'h3': out.append(f'<h3>{esc(b[1])}</h3>')
        elif k == 'img': out.append(f'<figure><img src="../img/{b[1]}" alt="{esc(b[2])}" loading="lazy"><figcaption>{esc(b[2])}</figcaption></figure>')
        elif k == 'ul': out.append('<ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul>')
        elif k == 'tip': out.append('<div class="tip"><b>小贴士</b><ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul></div>')
        elif k == 'stay': out.append(f'<aside class="stay"><h2>住在海边</h2><p>{esc(b[1])}</p><div class="btns"><a class="btn solid" href="../#book">看怎么预订</a><a class="btn line" href="../#rooms">看看房间</a></div></aside>')
    return '\n'.join(out)

def build_site():
    for i, a in enumerate(A):
        url = f'{SITE}/fz/{a["slug"]}.html'; nxt = A[(i + 1) % len(A)]; cv = cover_of(a)
        page = HEAD.format(title=esc(a['title']), desc=esc(a['desc']), url=url, ogtype='article', img=f'{SITE}/img/{cv}')
        cov = '' if any(b[0]=='img' and b[1]==cv and imgok(b) for b in a['body'][:6]) else f'<figure class="cover"><img src="../img/{cv}" alt="{esc(a["cover_alt"])}"></figure>'
        page += f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">福州攻略</a></p>
    <h1>{esc(a['title'])}</h1>
    {cov}
{render(a['body'])}
    <p class="next">下一篇：<a href="{nxt['slug']}.html">{esc(nxt['title'])}</a></p>
  </div>
</main>
''' + FOOT
        open(f'{OUT}/{a["slug"]}.html', 'w').write(page)
    cards = '\n'.join(f'''    <a class="gcard" href="{a['slug']}.html">
      <img src="../img/{cover_of(a)}" alt="{esc(a['cover_alt'])}" loading="lazy">
      <h2>{esc(a['title'].split('：')[0])}</h2>
      <p>{esc(a['desc'])}</p>
    </a>''' for a in A)
    idx = HEAD.format(title='福州吃喝玩乐攻略', desc='福州怎么吃、怎么逛：48小时美食路线、3天行程建议、免费景点、小众好去处、2日慢游，最后留一天去琅岐岛看海。', url=f'{SITE}/fz/', ogtype='website', img=f'{SITE}/img/hero.jpg')
    idx += f'''<main class="article">
  <div class="wrap">
    <p class="crumb"><a href="../">首页</a> / 福州攻略</p>
    <h1>福州吃喝玩乐攻略</h1>
    <p class="lead">来琅岐岛之前，先在福州市区吃一圈、逛一圈。这里是常被客人问到的吃喝和路线；岛上怎么玩，看<a href="../guide/">琅岐岛攻略</a>。</p>
    <div class="gcards">
{cards}
    </div>
  </div>
</main>
''' + FOOT
    open(f'{OUT}/index.html', 'w').write(idx)

def plain(blocks, for_xhs=True):
    """小红书正文：去掉图片块，h3 用【】，列表用 · """
    out = []
    for b in blocks:
        k = b[0]
        if k == 'img': continue
        if k == 'h2': out.append('\n' + b[1])
        elif k == 'h3': out.append('【' + b[1] + '】')
        elif k == 'p': out.append(b[1].replace('<a href="langqi-island.html">', '').replace('</a>', ''))
        elif k in ('ul',): out += ['· ' + x for x in b[1]]
        elif k == 'tip': out += ['小贴士：'] + [f'{n}. {x}' for n, x in enumerate(b[1], 1)]
        elif k == 'stay': out.append(b[1])
    return '\n'.join(out).strip()

def images_of(a):
    seen = []
    for b in a['body']:
        if b[0] == 'img' and b[1] not in seen: seen.append(b[1])
    return seen

def export_notes(dest):
    for a in A:
        d = f'{dest}/第{a["no"]}篇_{a["slug"]}'
        os.makedirs(d, exist_ok=True)
        imgs = images_of(a)
        lines = [f'【标题】\n{a["xhs_title"]}\n', '【正文】\n' + plain(a['body']) + '\n', '【话题】\n' + a['tags'] + '\n',
                 '【图片顺序】（福州的图在 03_文案 文件夹；琅岐和民宿的图可从官网图片地址保存，或用 01_宣传精选 里的同类照片）']
        for n, im in enumerate(imgs, 1):
            src = ('03_文案\\' + im[3:].replace('yantaishan.jpg','yantaishan.webp')) if im.startswith('fz/') else ('官网图片 youfuhaishu.com/img/' + im)
            lines.append(f'{n:02d}. {src}')
        lines.append('\n【官网同篇】' + f'{SITE}/fz/{a["slug"]}.html')
        open(f'{d}/小红书文案.txt', 'w', encoding='utf-8-sig').write('\n'.join(lines))
        # 抖音图文：短
        hs = [b[1] for b in a['body'] if b[0] in ('h2', 'h3')][:8]
        dy = [a['xhs_title'], '', a['body'][0][1], ''] + [f'📍{h}' for h in hs if '海边' not in h and '琅岐' not in h] + ['', '最后留一天去琅岐岛看海，门口就是沙滩。', '', a['tags']]
        open(f'{d}/抖音图文文案.txt', 'w', encoding='utf-8-sig').write('\n'.join(dy) + '\n\n【图片顺序】同小红书，抖音图文最多放 35 张，建议 6–9 张。')

if __name__ == '__main__':
    build_site()
    if len(sys.argv) > 1: export_notes(sys.argv[1])
    print('ok', [cover_of(a) for a in A])
