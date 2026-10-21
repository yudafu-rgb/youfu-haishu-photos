# 有福海墅 · 项目说明（给 AI 看）

福州琅岐岛「有福海墅」海边别墅民宿的照片库 + 官网。官网 https://youfuhaishu.com/ 是 GitHub Pages，源码在 `docs/`，**推到 main 就是上线**（一两分钟生效）。

**这是公开仓库**：不要写进经营底细（超订、自住、底价、平台口径差异）、密码、token。

## 先看哪里

| 文件 | 用途 |
| --- | --- |
| `物业信息.md` | **房东确认过的事实**。写任何页面、文案前先查这里；这里没有的事实不要编，问房东 |
| `网站协作记录表.md` | 几个 AI 一起改网站。动手前登记要改的文件，改完写结果（最新的写在表头下第一行） |
| `内容日历.md` | 每周一篇攻略的排期和「待核实」 |
| `README.md` | 照片目录说明 |

## 目录

- `docs/`：网站。`guide/` 琅岐攻略，`fz/` 福州攻略，`en/` 英文版，`img/` 网站用图，`video/` 网站视频
- `工具/`：脚本（见下面「自动化」和「别碰」）
- 其余中文目录（`宣传精选/`、各栋实拍、`视频/`、`meituan/` 等）：原始素材，不直接上网站

## 自动化（GitHub Actions，跑在 GitHub 上，不花 Claude 额度）

| 工作流 | 什么时候跑 | 做什么 |
| --- | --- | --- |
| `daily-today.yml` | 北京时间 0:10、6:10、12:10、18:10 | 运行 `工具/build_today.py`，生成 `docs/guide/today.html`（日出日落、天气、月相、潮汛、台风）、`docs/guide/caizhai.html`（采摘日历）、`docs/daily.js`（首页大图轮换、近期提示），用 `工具/sitemap_lastmod.py` 把 sitemap 每页日期改成最后提交日期；只有 0:10 那次推百度 |
| `push-index.yml` | main 上 `docs/**.html` 有改动 | `工具/push_index.py` 把改动页面推百度（每次最多 5 条）和 IndexNow |
| `site-check.yml` | 每周一 9:00、每次改 docs | `工具/check_site.py`：死链、图片超 800KB、漏统计代码、sitemap 漏页、价格和 `price.html` 对不上、优惠过期还挂着；有问题开 Issue |
| `uptime.yml` | 每小时 | 官网打不开、HTTPS 证书 14 天内到期、域名 30 天内到期（现在到 2027-10-15）就开 Issue「官网告警」，恢复自动关 |
| `reminders.yml` | 每天 8:50 | `工具/reminders.py`：周一提醒内容日历本周那篇、每月 1 号提醒当月采摘、除夕前 21 天换平台春节标题、除夕前 10 天查灯会地点、农历二月初一换回标题 |
| `upload-check.yml` | 推了照片、视频 | `工具/check_uploads.py`：带 GPS / 手机型号、超过 50MB 就开 Issue |

- 提醒都走 GitHub Issue（标签「自动提醒」，`工具/issue.py`），GitHub 会发邮件给房东。
- 价格只改 `docs/price.html`，其他页面的价格要和它一致，不然体检会报。
- 百度 token 在仓库 Secrets 的 `BAIDU_TOKEN`；百度每天配额约 10 条，别浪费。
- `docs/8cf8b6e8940616fad9620bc4f4c5677a.txt` 是 IndexNow 的 key 文件，**别删**。
- 外部数据：Open-Meteo（天气、海洋模型）、日本气象厅（台风路径），都免费无 key，拿不到就跳过那一块，页面照常生成。
- 能做成定时自动跑的事，优先写成 GitHub Actions，不要每次靠 AI 手动做。

## 硬规则

**新页面**
1. `<head>` 里带统计代码：从 `docs/index.html` 复制「流量统计：百度统计 + Google Analytics」那一段，原样。
2. 加进 `docs/sitemap.xml`；攻略页再加进 `docs/guide/index.html` 的卡片。
3. 页尾带悬浮微信和**新版**手机底部条（注释是「手机端底部固定咨询条：咨询空房 / 加微信 / 团建包栋 / 导航到店」），最省事是复制 `docs/guide/bishu.html` 的页头页脚。
4. 改了 `docs/style.css` 就把全站 `style.css?v=` 的版本号一起改掉，不然手机浏览器会用旧样式。
5. 推之前跑 `python3 工具/check_site.py`，要「全部正常」。

**别碰**
- `工具/build_guides.py`、`工具/build_fz.py` **已经落后于线上页面**，重跑会冲掉统计代码等后来的修改，而且路径写死在 `/tmp/claude-0/s/repo`。要改攻略页就直接改 HTML。
- `docs/guide/today.html`、`docs/guide/caizhai.html`、`docs/daily.js` 是自动生成的，手改会被覆盖。要改就改 `工具/build_today.py`：
  - 采摘品种和月份：`PICKING`、`SEAFOOD`
  - 首页大图轮换：`工具/hero_photos.txt`（一行一个 `docs/img/` 下的文件名）
  - 精确潮时和赶海窗口：`TIDE_PUBLISH`，**和潮汐表对比确认准了才打开**
- 首页「近期提示」（`#season-note`）的内容也在 `build_today.py` 的 `notices()` 里，节日按农历自动算，不用每年改日期。

**事实和写法**
- 价格以 `docs/price.html` 为准；坐标 JSON-LD 用 WGS-84（26.063260, 119.637902），高德/小程序用 GCJ-02（26.059977, 119.642365），两套别混。
- 厨房只有包栋和长住客人能用；泳池是度假村游乐场的、只在 7–9 月开；打铁花、火壶场次不固定。更多见 `物业信息.md`。
- 网上查到的事实（节日、休渔、葡萄季等）在 `物业信息.md` 里记下来源。

## 和房东沟通

- 用中文，说大白话，少用技术词。
- 房东在意 Claude 额度：大活先说清楚大概要做什么，能用 GitHub 免费跑的就别用 AI。
- 要房东确认事实时，一次问一项，给 A/B/C 选项，房东回一个字母就行。
- 搜到的信息附来源链接；查不到的就说查不到，不要猜。

## 写代码的四条规矩

改编自 [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)（MIT 许可，Forrest Chang），原文是英文。

1. **先想再写**：把假设说出来；有几种理解就摆出来，别悄悄挑一个；有更简单的办法就说；没弄明白就停下来问。
2. **简单优先**：只写解决问题需要的最少代码。不加没要求的功能、不为只用一次的代码搞抽象、不为不可能发生的情况写处理。写了 200 行能用 50 行解决，就重写。
3. **只动该动的**：不顺手"改进"旁边的代码、注释、格式；不重构没坏的东西；照着现有风格写。看到无关的问题，说出来，不要直接删。自己改出来的没用的东西，自己清掉。
4. **定好怎样算做完**：动手前说清楚怎么验证（比如 `check_site.py` 全部正常、手机宽度 375px 不横向滚动、截图看过），做完验证了再说完成。
