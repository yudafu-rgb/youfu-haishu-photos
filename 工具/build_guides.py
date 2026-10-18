# -*- coding: utf-8 -*-
# Builds docs/guide/*.html from the article list below.
import html, os, datetime
OUT = '/tmp/claude-0/s/repo/docs/guide'
SITE = 'https://youfuhaishu.com'
os.makedirs(OUT, exist_ok=True)

# Each body is a list of blocks: ('p', text) | ('h2', text) | ('img', file, alt) | ('ul', [items]) | ('tip', [items])
A = [
dict(slug='langqi-drive', title='琅岐轻自驾慢逛线：半天到一天刚刚好', short='琅岐轻自驾慢逛线',
 desc='福州周边周末去哪：开车上琅岐岛，看江海交界的堤岸、岛上田园和村镇。福州市区约 40 分钟，半天到一天的路线、吃饭、停车和出发前提醒，9 张攻略卡一次看完。',
 cover='lq-card-01', cover_alt='琅岐轻自驾慢逛线：半天到一天，适合周末慢慢逛',
 body=[
 ('p','琅岐这条线不靠「网红感」，靠的是轻松：江海交界的堤岸、岛上的田园、村镇里的烟火气，开车边走边看，半天到一天刚好。下面 9 张卡，按顺序看就能出发。'),
 ('h2','先看适不适合去'),
 ('img','lq-card-02','适合和不太适合去琅岐的人'),
 ('ul',['适合：周末想开车散心、想轻松看风景不赶景点、喜欢田园感和江海交界的人。','不太适合：想一次打卡很多景点、想走「超出片网红路线」的人。']),
 ('p','琅岐不是那种碧海蓝天大沙滩的海岛。不过想踩沙子也有地方：龙鼓度假村门口就是金鸡报晓海滩，退潮还能<a href="ganhai.html">赶海</a>。'),
 ('h2','从福州怎么去最顺'),
 ('img','lq-card-03','从福州去琅岐，自驾最合适'),
 ('p','自驾最合适。福州市区开车约 40 分钟（看路况），过跨江大桥就上岛。看到舒服的堤岸、田园、村镇，随时停下来。不自驾也可以打车上岛，就是没那么灵活。'),
 ('h2','路线总览'),
 ('img','lq-card-04','琅岐一天的路线总览'),
 ('ul',['推荐顺序：进岛 → 江边 / 海边堤岸 → 田园路慢开 → 村镇慢逛 → 找地方吃饭 → 再环一小段 → 返程。','半天轻松版：进岛 → 看江海风景 → 田园慢开 → 吃饭 → 回程。','一天完整版：进岛 → 堤岸风景 → 田园 / 村镇慢逛 → 午饭 → 下午继续绕岛看风景 → 傍晚返程。']),
 ('h2','一天这样安排最舒服'),
 ('img','lq-card-05','上午、中午、下午、傍晚的安排'),
 ('ul',['上午：从福州出发进岛，先看一段江海交界的风景，慢慢开，不急着打卡。','中午：在村镇或岛上餐馆吃饭，海鲜、家常菜、本地小吃都行。','下午：沿路继续慢逛，看田园、公路、村镇、堤岸。','傍晚：差不多了就返程，不用把行程排太满。']),
 ('h2','琅岐好看的，是这种气质'),
 ('img','lq-card-06','琅岐的江海、田园、公路和村镇'),
 ('ul',['江海交界：水面开阔，视野很舒服。','岛上田园：比起景点，更适合看路上的风景。','轻自驾公路：边开边停，路本身就有意思。','乡镇慢生活：村镇街巷、码头，日常的烟火气。','周末放空：不赶路的时候，这条线更耐看。']),
 ('h2','琅岐吃什么更稳'),
 ('img','lq-card-07','琅岐的海鲜、家常菜和小吃'),
 ('ul',['海鲜、河鲜家常做法：顺路吃，讲究新鲜。','岛上家常菜：简单实在。','福州小吃顺带安排，不用专门跑远。','时令水果、乡镇风味：看到合适的顺手买。']),
 ('p','点菜挑当天新鲜的，别一下点太多；周末吃饭可以错开饭点。'),
 ('h2','怎么走更省心'),
 ('img','lq-card-08','交通和停车建议'),
 ('ul',['自驾最推荐，打车也行，公交能到但适合不赶时间的人。','停车找村镇周边、公共区域和规范车位，别停在窄路、转弯口和居民出入的地方。','周末车会多一点，放慢节奏。']),
 ('h2','去之前先看这几个提醒'),
 ('img','lq-card-09','出发前的几个提醒'),
 ('tip',['把它当「轻自驾慢逛线」，别按纯海边度假线期待。','别把行程排太满，半天到一天最合适。','天气不好时体验会打折，出发前看看天气。','别只盯着打卡点，好看的常常在路上。','周末尽量早点出发。','想多待一晚，就住在海边，第二天早上去沙滩走走。']),
 ]),
dict(slug='langqi-island', title='琅岐岛周末攻略：福州人的私藏小海岛', short='琅岐岛周末攻略',
 desc='福州市区开车约 40 分钟的琅岐岛怎么玩：红光湖、金鸡报晓海滩、风水林、红蟳公社、罗汉石像小路、码头和金牌山炮台，附两三天玩法和必吃。',
 cover='g-bridge', cover_alt='从琅岐岛山上看闽江口和跨江大桥',
 body=[
 ('p','不想去人挤人的平潭？从福州市区开车约 40 分钟，就有一座人少、安静的小海岛——琅岐岛。遛娃、团建、散心都合适，周末两天刚好。'),
 ('h2','红光湖公园'),
 ('p','岛上的大湖公园，有环湖步道和大草坪，带孩子散步、野餐都很舒服。'),
 ('h2','龙鼓度假村 · 金鸡报晓海滩'),
 ('p','琅岐看海的好地方，视野开阔。白天踩浪拍照，傍晚看日落，退潮还能去赶海，捡小螃蟹、小贝壳。'),
 ('p','远处闽江口那几座小岛叫「五虎守门」，海里的礁石叫「白猴镇江」，都是有名字的风景。'),
 ('img','g-rock','海边的大礁石，退潮后露出沙滩'),
 ('p','度假村里还有一片沙丘上的古朴树林，本地人叫「风水林」。林子里有木栈道，夏天走进去很凉快；也可以坐乌篷船转一圈。'),
 ('img','g-boardwalk','防风林里的木栈道'),
 ('h2','红蟳公社'),
 ('p','海岛上的田园打卡地，乡村风光很治愈，适合全家慢慢逛。'),
 ('h2','山上的罗汉石像小路'),
 ('p','台阶两边藏着一尊尊罗汉像，爬到山顶能看到整片海和跨江大桥。'),
 ('h2','码头'),
 ('p','渔船回港的时候最热闹，海鲜很新鲜。'),
 ('img','g-port','琅岐岛码头'),
 ('h2','金牌山炮台'),
 ('p','清代的海防炮台，林则徐主持重修过，站在上面看闽江口。从龙鼓度假村开车约 20 分钟。'),
 ('h2','两三天怎么玩'),
 ('p','船政文化 → 闽安古镇 → 琅岐岛，人文和山海一次玩够。'),
 ('h2','必吃'),
 ('p','琅岐红蟳、梭子蟹，还有海蛎饼、鱼丸这些本地小吃。'),
 ('h2','交通'),
 ('p','自驾最方便，岛上景点之间开车都很近。'),
 ]),
dict(slug='langqi-one-day', title='琅岐岛一日游：山顶看海、罗汉石像小路、码头', short='琅岐岛一日游路线',
 desc='琅岐岛一天怎么玩：早上海边看日出，上午爬山看罗汉石像，中午码头看渔船，下午古牌坊碑亭，傍晚天台吹海风。',
 cover='g-town', cover_alt='山顶俯瞰琅岐镇',
 body=[
 ('p','琅岐岛一天就能玩完：早上看海，上午爬山，中午逛码头，傍晚回天台。下面是我们自己走过的顺序，不赶路。'),
 ('h2','早上：海边看日出'),
 ('p','从龙鼓度假村出门就是沙滩。七点前人少，风也凉。'),
 ('h2','上午：爬山找罗汉石像'),
 ('p','山里有条台阶小路，两边立着一尊尊罗汉石像，有的骑象，有的打坐，表情各不相同。爬到山顶，能看到整个琅岐镇和跨江大桥。'),
 ('img','g-luohan','山路边的罗汉石像'),
 ('h2','中午：码头看渔船卸货'),
 ('p','渔船靠岸时去码头转一圈，螃蟹刚从船上搬下来，还在筐里爬。'),
 ('img','g-crab','刚买的螃蟹'),
 ('h2','下午：古牌坊、古碑亭'),
 ('p','岛上留着不少老牌坊和碑亭，旁边有大树，下午走在树荫里不晒。'),
 ('img','g-pavilion','山脚的古亭'),
 ('h2','傍晚：天台吹海风'),
 ('p','回到住处上三楼天台，晚上坐着吹风，能听到海浪声。'),
 ('tip',['山路全是台阶，穿运动鞋。','夏天带水，做好防晒。']),
 ]),
dict(slug='ganhai', title='福州赶海攻略：琅岐岛退潮后的海滩', short='福州赶海攻略',
 desc='在福州琅岐岛龙鼓度假村金鸡报晓海滩赶海：怎么查潮汐、穿什么鞋、带什么，退潮后能捡到小螃蟹和小螺。',
 cover='g-tide1', cover_alt='退潮后在沙滩上赶海的住客',
 body=[
 ('p','琅岐岛龙鼓度假村的金鸡报晓海滩，退潮以后最好玩。石头缝、小水洼里会冒出小螃蟹、小螺，孩子能玩一下午。'),
 ('img','g-tide2','蹲在沙滩上找螃蟹'),
 ('h2','几个提醒'),
 ('ul',['出发前查潮汐：天气 App 搜「琅岐 潮汐」，退潮前后两小时最合适。','穿防滑的鞋，礁石很滑。','防晒、帽子、一套换洗衣服都带上。','小的放生，垃圾带走。']),
 ('h2','赶完海别急着走'),
 ('p','退潮后的沙滩又平又软，捡根树枝写个名字、画颗爱心，等浪慢慢漫上来，拍照特别好看。'),
 ('p','有福海墅就在海滩边，出门几分钟就到。没带小桶小铲也没关系，可以借，也能现买。玩累了回去冲个澡，上天台吹吹风。'),
 ('p','这页的赶海照片是住客拍的。'),
 ]),
dict(slug='sunset', title='琅岐岛看日落：山顶、码头、沙滩和天台', short='琅岐岛看日落',
 desc='福州琅岐岛看日落的几个地方：岛上小山、码头、沙滩，以及海边别墅的三楼天台；附十月日落时间和拍照小贴士。',
 cover='g-dusk', cover_alt='傍晚的龙鼓度假村园区',
 body=[
 ('p','在福州待久了，总想找个地方安静看一场日落。琅岐岛离市区不远，傍晚的海边特别温柔。'),
 ('h2','岛上的小山'),
 ('p','爬到山顶能看到整片海、跨江大桥和镇子，天气好的时候特别出片。'),
 ('img','g-bay','山上看海湾'),
 ('h2','码头边'),
 ('p','渔船陆续回港，看渔民卸货、收网，很有烟火气。'),
 ('h2','沙滩'),
 ('p','退潮后沙滩很大，光脚踩着走一走。'),
 ('h2','天台'),
 ('p','有福海墅每栋三楼都有天台，晚饭后坐在上面吹风，看天一点点变成粉色、紫色。'),
 ('tip',['十月日落大概在傍晚 5 点半到 6 点之间，提前半小时到。','海边晚上风大，带件薄外套。','想拍剪影，等太阳快落下时逆光拍。']),
 ('h2','天黑以后'),
 ('p','别急着回去：沙滩上的灯亮起来，海边还有不少人在散步、踩水。'),
 ('img','g-nightbeach','夜里的海滩'),
 ]),
dict(slug='fishing-port', title='琅岐岛渔港：看渔船回港，挑点海鲜', short='琅岐岛渔港',
 desc='琅岐岛渔港怎么逛：看渔船回港卸货、买刚上岸的海鲜，了解琅岐红蟳和贴沙鱼；附去码头的时间和注意事项。',
 cover='g-harbor', cover_alt='琅岐岛港湾里的渔船',
 body=[
 ('p','来琅岐岛，除了沙滩，渔港也值得去转转。渔船靠岸的时候最热闹，很有海岛的烟火气。'),
 ('h2','码头'),
 ('p','一排排渔船停在港里，可以看渔民收网、卸货。'),
 ('img','g-port2','码头'),
 ('h2','海鲜'),
 ('p','刚上岸的螃蟹活蹦乱跳，在岛上吃海鲜很新鲜。'),
 ('p','琅岐红蟳在老福州人心里地位很高，坐月子都点名要它；还有一种扁扁的贴沙鱼，古时候拿去进贡，外号叫「皇帝鱼」。'),
 ('h2','从山上看'),
 ('p','从岛上的小山往下看，渔港、跨江大桥和镇子一览无余。傍晚渔船陆续回港，海面被夕阳染成橘色。'),
 ('tip',['码头地面湿滑，穿防滑的鞋。','想看热闹，下午到傍晚去。','海边风大太阳大，记得防晒。']),
 ]),
dict(slug='kids-beach', title='福州带娃去海边：琅岐岛挖沙、采摘、看日落', short='福州带娃去海边',
 desc='带孩子去福州琅岐岛海边：出门就是沙滩，退潮捡贝壳看小螃蟹，园子里免费摘洛神花和柠檬；附带娃要准备的东西。',
 cover='g-rainbow', cover_alt='海滩上的彩虹拱门',
 body=[
 ('p','带娃的周末，最怕排队和堵车。从福州市区开车约 40 分钟到琅岐岛，住处出门就是沙滩。'),
 ('h2','沙滩'),
 ('p','孩子拿个小铲子能挖一下午，退潮的时候还能捡贝壳、看小螃蟹。'),
 ('h2','园子'),
 ('p','别墅之间有花园和草地，孩子可以跑来跑去。'),
 ('h2','采摘'),
 ('p','园子里的洛神花、柠檬住客可以免费摘。红红的洛神花孩子特别爱摘，摘回来还能泡茶。'),
 ('img','g-roselle','园子里的洛神花'),
 ('h2','傍晚'),
 ('p','上三楼天台，一家人吹海风等日落。'),
 ('h2','带什么'),
 ('ul',['海边太阳大，帽子、防晒霜一定带。','给孩子备一套换洗衣服和拖鞋，玩沙玩水一定会湿。','没带小桶小铲也没关系，可以借，也能现买。']),
 ]),
dict(slug='group-trip', title='福州团建、聚会去哪：琅岐岛包一整栋海边别墅', short='团建聚会包栋',
 desc='十几个人的公司团建、同学会、家族聚会：在福州琅岐岛包一整栋海边别墅，5 间房、麻将牌桌、茶室、天台烧烤，附一天半的安排。',
 cover='g-mahjong', cover_alt='别墅一楼的麻将桌',
 body=[
 ('p','公司团建、同学聚会、家族出游，人一多就头疼：住得散、玩不到一块。包一整栋海边别墅，三层楼都是自己人，不用担心吵到别人。'),
 ('h2','一栋楼里有什么'),
 ('ul',['5 间房、9 张床。','一楼客厅：麻将桌、牌桌，不打牌的坐沙发聊天也不挤。','二楼：木茶桌、榻榻米、健身房，可以免费尝尝茉莉花茶。','三楼天台：户外桌椅，吹海风聊天。','烧烤架免费用，食材和炭自己带。','红花阁每间房都有投影，晚上可以一起看电影。','整栋包下来还能用餐厅自己做饭。']),
 ('h2','一天半怎么安排'),
 ('ul',['下午到，先去门口沙滩玩游戏、拍大合照。','傍晚上天台，边吃边聊看日落。','晚上麻将、桌游、茶话会各选各的。','第二天睡到自然醒，去岛上爬山看海再回城。']),
 ('p','福州市区开车约 40 分钟，离长乐机场约 30 分钟，外地同事过来也方便。'),
 ]),
dict(slug='fuzhou', title='福州旅游攻略：第一次来照着走不踩坑', short='福州旅游攻略',
 desc='第一次来福州怎么玩：三坊七巷、鼓山、福道、上下杭和烟台山、闽江夜游，必吃小吃和交通小贴士；想看海就多留一天去琅岐岛。',
 cover='g-bridge', cover_alt='闽江口和跨江大桥',
 body=[
 ('p','第一次来福州，不用做太复杂的攻略。古厝、江景、森林步道、地道小吃，照着这几个地方走就够了。'),
 ('h2','三坊七巷'),
 ('p','福州的名片，街区免费逛。主街比较热闹，真正好看的在安静的支巷里，文儒坊、黄巷很适合拍照。故居和博物馆很多周一闭馆，建议上午去，人少光线好。'),
 ('h2','鼓山'),
 ('p','本地人最爱的爬山去处。推荐坐缆车上山省力，再走路下山，沿途看摩崖石刻。'),
 ('h2','福道'),
 ('p','城市里的悬空森林步道。傍晚去最舒服，风凉光线也好；下雨天路面滑，注意安全。'),
 ('h2','上下杭和烟台山'),
 ('p','白天普通，晚上灯一亮就很出片。烟台山全是坡路，一定穿平底鞋。'),
 ('h2','闽江夜游'),
 ('p','晚上坐船看两岸夜景，节假日记得提前约。'),
 ('h2','必吃'),
 ('p','小吃：鱼丸、肉燕、锅边糊、捞化、海蛎饼。正餐：荔枝肉、南煎肝、佛跳墙。景区主街偏贵，往巷子里找本地老店。'),
 ('tip',['坐火车首选福州站，离市区近。','老城区停车难，地铁加单车更方便。','门票、开放时间以官方为准。']),
 ('h2','想看海就多留一天'),
 ('p','从福州市区开车约 40 分钟到琅岐岛，人少海美。怎么玩看这篇：<a href="langqi-island.html">琅岐岛周末攻略</a>。'),
 ]),
dict(slug='roselle', title='琅岐岛的秋天：海边园子里的洛神花红了', short='秋天摘洛神花',
 desc='秋天在福州琅岐岛有福海墅的园子里免费摘洛神花和柠檬：怎么挑、怎么泡茶，带孩子摘要注意什么。',
 cover='g-roselle2', cover_alt='挂满枝头的洛神花',
 body=[
 ('p','秋天来琅岐岛，除了看海，还多了一件小事——摘洛神花。'),
 ('p','有福海墅的园子里有一片洛神花，秋天正红。一颗颗红色的花萼挂满枝头，远看像一树小灯笼。'),
 ('h2','怎么摘、怎么吃'),
 ('ul',['住客可以免费摘，挑颜色深红、饱满的。','花萼剥下来洗干净，泡水就是酸酸甜甜的红色花茶，加点冰糖或蜂蜜更好喝。','旁边还有几棵柠檬树，青柠檬切片泡水也很清爽。']),
 ('img','g-lemon','园子里的柠檬树'),
 ('h2','小提醒'),
 ('ul',['洛神花的花萼底部有点扎手，摘的时候小心。','摘适量就好，给后面的客人也留一些。','摘完去门口沙滩吹吹海风，傍晚上天台看日落。']),
 ]),
dict(slug='jasmine-tea', title='在琅岐海边，用木茶桌泡一壶茉莉花茶', short='海边喝茉莉花茶',
 desc='福州茉莉花茶窨制手艺有上千年。在琅岐岛有福海墅二楼茶室免费尝茉莉花茶，园子里的洛神花也能自己摘来泡。',
 cover='g-tea', cover_alt='二楼茶室的木茶桌',
 body=[
 ('p','福州人的一天，从一杯茉莉花茶开始。福州茉莉花茶窨制的手艺有上千年，还被列入了全球重要农业文化遗产。'),
 ('h2','二楼茶室'),
 ('p','有福海墅最安静的角落，是二楼的茶室：木茶桌、几把椅子，窗外是绿树和海风。'),
 ('ul',['茶室备了茉莉花茶，住客可以免费尝，泡开以后满屋都是花香。','园子里的洛神花也能自己摘，泡出来是酸酸甜甜的红色花茶。','隔壁是榻榻米，喝完茶躺一会儿。','傍晚再上三楼天台，看天色慢慢变暗。']),
 ('p','不赶景点，就是来喝茶、吹风、发呆的。'),
 ]),
]

def esc(s): return html.escape(s, quote=True)

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
<link rel="stylesheet" href="../style.css?v=20261018a">
</head>
<body>
<header class="bar solid">
  <a class="brand" href="../" aria-label="有福海墅 首页"><img src="../img/logo.png" alt="">有福海墅</a>
  <nav aria-label="页面导航">
    <a href="../#rooms">房型</a>
    <a href="./">琅岐攻略</a>
    <a href="../fz/">福州攻略</a>
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
CTA = '''<aside class="stay">
  <h2>住在有福海墅</h2>
  <p>龙鼓度假村里的三栋海边别墅，出门就是沙滩。可订单间，也可整栋包下。</p>
  <a class="btn solid" href="../#book">看怎么预订</a>
  <a class="btn line" href="../#rooms">看看房间</a>
</aside>
'''

def render_body(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p': out.append(f'<p>{b[1]}</p>')  # trusted text; may contain a link
        elif k == 'h2': out.append(f'<h2>{esc(b[1])}</h2>')
        elif k == 'img':
            cls = ' class="card"' if b[1].startswith('lq-card') else ''
            out.append(f'<figure{cls}><img src="../img/g/{b[1]}.jpg" alt="{esc(b[2])}" loading="lazy"></figure>')
        elif k == 'ul': out.append('<ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul>')
        elif k == 'tip': out.append('<div class="tip"><b>小贴士</b><ul>' + ''.join(f'<li>{esc(i)}</li>' for i in b[1]) + '</ul></div>')
    return '\n'.join(out)

for i, a in enumerate(A):
    url = f'{SITE}/guide/{a["slug"]}.html'
    others = [o for o in A if o is not a][:0]
    nxt = A[(i + 1) % len(A)]
    page = HEAD.format(title=esc(a['title']), desc=esc(a['desc']), url=url, ogtype='article', img=f'{SITE}/img/g/{a["cover"]}.jpg')
    page += f'''<main class="article">
  <div class="wrap narrow">
    <p class="crumb"><a href="../">首页</a> / <a href="./">游玩攻略</a></p>
    <h1>{esc(a['title'])}</h1>
    <figure class="cover{' card' if a['cover'].startswith('lq-card') else ''}"><img src="../img/g/{a['cover']}.jpg" alt="{esc(a['cover_alt'])}"></figure>
{render_body(a['body'])}
{CTA}
    <p class="next">下一篇：<a href="{nxt['slug']}.html">{esc(nxt['title'])}</a></p>
  </div>
</main>
'''
    page += FOOT
    open(f'{OUT}/{a["slug"]}.html', 'w').write(page)

# index
cards = '\n'.join(f'''    <a class="gcard" href="{a['slug']}.html">
      <img{' class="top"' if a['cover'].startswith('lq-card') else ''} src="../img/g/{a['cover']}.jpg" alt="{esc(a['cover_alt'])}" loading="lazy">
      <h2>{esc(a['short'])}</h2>
      <p>{esc(a['desc'])}</p>
    </a>''' for a in A)
idx = HEAD.format(title='琅岐岛、福州游玩攻略', desc='琅岐岛怎么玩、福州赶海、看日落、渔港海鲜、带娃去海边、团建包栋、福州市区攻略。有福海墅整理的本地游玩攻略。', url=f'{SITE}/guide/', ogtype='website', img=f'{SITE}/img/hero.jpg')
idx += f'''<main class="article">
  <div class="wrap">
    <p class="crumb"><a href="../">首页</a> / 游玩攻略</p>
    <h1>琅岐岛、福州游玩攻略</h1>
    <p class="lead">我们在琅岐岛住久了，把客人常问的地方写下来：怎么玩、什么时候去、要带什么。</p>
    <div class="gcards">
{cards}
    </div>
  </div>
</main>
'''
idx += FOOT
open(f'{OUT}/index.html', 'w').write(idx)

# sitemap + robots
today = datetime.date.today().isoformat()
urls = [f'{SITE}/', f'{SITE}/en/', f'{SITE}/juhuage.html', f'{SITE}/honghuage.html', f'{SITE}/meiguige.html', f'{SITE}/tuanjian.html', f'{SITE}/price.html', f'{SITE}/en/price.html', f'{SITE}/guide/'] + [f'{SITE}/guide/{a["slug"]}.html' for a in A]
import glob
fz=sorted(glob.glob('/tmp/claude-0/s/repo/docs/fz/*.html'))
urls += [f'{SITE}/fz/'] + [f'{SITE}/fz/{os.path.basename(f)}' for f in fz if not f.endswith(('index.html','credits.html'))]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls) + '</urlset>\n'
open('/tmp/claude-0/s/repo/docs/sitemap.xml', 'w').write(sm)
open('/tmp/claude-0/s/repo/docs/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print('ok', len(A))
