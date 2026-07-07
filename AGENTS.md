AGENTS.md
用户更新要求（2026-07-06）

本项目只做客观信息聚合，不做主观投资判断，不提供交易建议、操作方向、建仓/平仓建议或具体交易执行建议。

每日收集范围包括：

- Capesize 市场公开信息
- 研报摘要
- 相关行业新闻
- 公司动态
- 矿山新闻及动态
- 澳洲 Pilbara 每日发运量，优先从 Pilbara Ports 公开信息获取
- 中国需求：高炉开工率、铁水产量、钢厂利润、港口库存、铁矿库存
- 天气：澳洲、巴西、几内亚及中国主要港口天气
- 商品价格：铁矿石、铝矾土、动力煤、焦煤、氧化铝
- 燃油价格：新加坡、舟山、鹿特丹高硫和低硫燃油

重点矿山及公司：

- 铁矿：BHP、Vale、FMG、Rio Tinto、Roy Hill、CSN、Anglo American、西芒杜相关项目
- 铝矾土：几内亚、澳洲、巴西及其他主要铝矾土矿山和出口项目

所有信息必须保留来源、链接、发布时间或数据日期、采集时间。缺失数据不得补造，未验证信息必须标注。

1. 项目目标

本项目用于每日收集、整理和分析与 Capesize 市场相关的信息。

Agent 的核心任务不是简单罗列新闻，而是客观回答：

今天收集到了哪些 Capesize 相关公开数据？
这些数据来自哪些来源，数据日期和发布时间是什么？
哪些信息是精确数值，哪些只是新闻或研报摘要？
哪些关键数据未取得公开可验证数值？
哪些来源或数据需要后续继续核对？

第一阶段暂不使用 AIS 船位数据，也不采集 FFA Recap。

2. 研究范围

重点研究以下内容：

现货市场
BCI
C5TC
C3
C5
C7
C14
C16
Atlantic 和 Pacific 市场表现
主要货盘变化
船东报价变化
成交速度
船货匹配情况
公开 FFA 市场数据

仅在能够从合法、可靠、结构化来源获取时研究：

Capesize 5TC
近月合约
次月合约
季度合约
Calendar 合约
日涨跌
成交量
Open Interest
期限结构
月差和季差

不读取、不解析、不依赖：

FFA Recap 邮件
经纪商 Recap
聊天软件中的 FFA 成交转述
未验证的场外交易记录
货物需求
澳洲铁矿发运
巴西铁矿发运
南非铁矿发运
几内亚铝土矿发运
煤炭长航线货盘
矿山检修和生产变化
主要矿商销售和发运指引
中国需求
铁矿石港口库存
铁水产量
高炉开工率
钢厂利润
钢材库存
钢材需求
中国铁矿石进口
铁矿石价格变化
其他影响因素
港口拥堵
天气
台风和飓风
港口关闭
罢工
矿山事故
航道中断
燃油价格
新船交付
拆船
环保政策
中国及全球宏观政策

除非会明显影响 Capesize 市场，否则不重点研究：

集装箱航运
油轮市场
小型散货船市场
与钢铁、矿石和航运无关的普通宏观新闻
与 Capesize 无直接关系的公司新闻
3. 信息源优先级
一级来源

优先使用原始和官方信息：

Baltic Exchange
港口官方数据
海关数据
矿山公司公告
上市公司公告
交易所数据
清算所数据
政府部门数据
公司财报
公司生产报告
二级来源

可信行业媒体和数据机构：

Reuters
Bloomberg
Fastmarkets
Argus
Mysteel
S&P Global
TradeWinds
Lloyd's List
Splash247
三级来源

市场参考信息：

航运市场评论
行业研究报告
船舶经纪市场评论
行业人士公开观点
低优先级来源
社交媒体
论坛
未署名转述
未经验证的市场传闻
私人聊天记录

重要结论应尽量由一级或二级来源验证。

未经证实的信息必须标记：

未验证

不得把单一市场观点或市场传闻写成确定事实。

4. 每日工作流程

Agent 每日按以下顺序工作：

收集当天现货市场数据和相关新闻
收集公开可验证的 FFA 市场数据
提取价格、成交量、货盘、发运和中国需求数据
删除重复新闻和重复数据
核对发布日期和事件发生日期
判断每条信息的影响方向
判断影响对象和影响周期
检查不同信息之间是否互相验证
生成每日市场报告
保存原始数据和最终报告
5. 数据字段
公开 FFA 数据

仅在数据可合法、稳定获取时保存：

date
contract
contract_month
bid
offer
last
settlement
daily_change
daily_change_pct
volume
open_interest
source
source_url
collected_at

如果没有成交量或 Open Interest，不得自行估算。

如果来源只提供价格，不得推断买卖方向。

现货市场数据
date
BCI
C5TC
C3
C5
C7
C14
C16
daily_change
weekly_change
source
source_url
collected_at
发运和货盘数据
date
country
port
commodity
shipment_volume
cargo_size
destination
loading_window
source
source_url
collected_at
中国需求数据
date
port_inventory
hot_metal_output
blast_furnace_rate
steel_margin
steel_inventory
iron_ore_import
source
source_url
collected_at
新闻和事件数据
published_at
event_date
title
summary
region
affected_market
impact_direction
impact_horizon
impact_strength
confidence
source
source_url
6. 数据清洗规则
所有时间统一使用 Asia/Singapore。
重量统一使用吨。
运价统一使用美元/天或美元/吨。
百分比格式在项目内保持一致。
同一新闻被多个网站转载时，优先保留原始来源。
同一事件多次更新时，保留最新状态，并记录历史变化。
不得使用没有明确日期的数据解释当前市场。
发布时间和事件发生时间必须分开记录。
缺失数据必须保留为空，不得随意填充。
自动推断的信息必须标记：
inferred = true
市场传闻必须标记：
verified = false
所有数据必须保留来源和采集时间。
私人邮件和聊天记录不得作为默认数据源。
无法确认来源的数据不得进入核心数据库。
7. 信息分类规则

每条重要信息必须标记以下内容。

信息性质
事实数据
公司动态
行业新闻
研报摘要
天气事件
价格变化
缺失数据

涉及市场或对象
Spot
FFA
BCI
C5TC
C3
C5
Atlantic
Pacific
矿山
港口
中国需求
商品价格
燃油价格

数据日期或事件日期
发布时间
来源名称
来源链接
采集时间
是否已验证
备注
8. 分析框架

每日分析应按以下顺序进行：

Spot Market
Public FFA Market Data
Cargo Demand
China Demand
Congestion and Weather
Macro and Events
Cross Validation
Final Market View

核心逻辑：

货物需求
×
运输距离
÷
有效运力
=
运价压力

第一阶段由于暂不使用 AIS 数据，有效运力主要通过以下信息间接判断：

港口拥堵
船东报价
现货成交速度
货盘数量
船货匹配情况
Atlantic 与 Pacific 市场强弱
航速和燃油变化
天气和港口延误
公开 FFA 期限结构
9. 客观摘要规则

日报摘要只回答：

今天收集到了哪些公开数据？
每条数据的日期、来源和链接是什么？
哪些数据是精确数值？
哪些数据只取得新闻或研报摘要？
哪些数据没有取得公开可验证数值？
哪些信息需要后续继续核对来源？

不得把信息摘要写成市场判断。
不得使用“偏多、偏空、强看多、强看空”等措辞。
不得输出综合评分。
不得输出交易含义、交易建议或仓位建议。

10. 每日报告格式
# Capesize Daily Market Report

## 1. 信息摘要

- 本日已取得的公开精确数据：
- 本日已取得的新闻和研报摘要：
- 本日未取得公开可验证数值的数据：
- 需要继续核对的来源：

## 2. Spot Market

- BCI：
- C5TC：
- C3：
- C5：
- Atlantic：
- Pacific：
- 主要现货变化：

## 3. Public FFA Market Data

- M1：
- M2：
- Quarter：
- Calendar：
- 成交量：
- Open Interest：
- 期限结构：
- FFA与现货是否一致：
- 数据完整度：

## 4. Cargo Demand

### Australia

- 发运：
- 货盘：
- 主要变化：

### Brazil

- 发运：
- 货盘：
- 主要变化：

### Other Cargoes

- 南非铁矿：
- 几内亚铝土矿：
- 煤炭：
- 其他长航线货物：

## 5. China Demand

- 港口库存：
- 铁水产量：
- 高炉开工率：
- 钢厂利润：
- 钢材库存：
- 铁矿价格：

## 6. Congestion, Weather and Events

- 港口拥堵：
- 天气：
- 矿山事件：
- 港口事件：
- 政策和宏观变化：

## 7. 价格变化

- 铁矿石：
- 铝矾土：
- 动力煤：
- 焦煤：
- 氧化铝：
- 新加坡燃油：
- 舟山燃油：
- 鹿特丹燃油：

## 8. 研报摘要

1.
2.
3.

## 9. 相关行业新闻和公司动态

1.
2.
3.

## 10. 缺失数据和后续核对

## 11. Data Quality

- 缺失数据：
- 未验证信息：
- 数据冲突：
- 需要继续核对的数据：

12. 禁止事项
不得虚构价格、成交量、货盘或发运量。
不得把预测写成确定事实。
不得使用旧新闻解释当前行情而不注明日期。
不得只看新闻标题。
不得把相关性直接写成因果关系。
不得把未经验证的传闻作为核心结论。
不得忽略相互矛盾的数据。
不得重复收录同一事件。
不得在数据不足时给出高置信度结论。
不得自动执行真实交易。
不得输出没有来源的精确数字。
不得为了形成结论而强行填补缺失数据。
不得读取或解析 FFA Recap 邮件。
不得依赖经纪商 Recap 作为核心数据源。
不得将聊天记录中的报价视为正式市场数据。
13. 项目目录
data/
├── raw/
├── processed/
└── reference/

reports/
├── daily/
└── weekly/

src/
├── collectors/
├── parsers/
├── signals/
└── reports/

config/
tests/
logs/

建议文件命名：

ffa_public_YYYY-MM-DD.csv
spot_YYYY-MM-DD.csv
cargo_YYYY-MM-DD.csv
china_demand_YYYY-MM-DD.csv
news_YYYY-MM-DD.json
cape_daily_report_YYYY-MM-DD.md
14. 代码规范
使用 Python 3.12 或以上版本
使用类型注解
外部请求必须设置 timeout
数据采集失败时必须记录日志
API Key 不得写入代码
敏感信息存放在 .env
每条数据必须保存 source、source_url 和 collected_at
解析失败的数据不得静默丢弃
重要计算应编写单元测试
修改数据结构时应保留兼容性或迁移脚本
优先输出结构化数据，再生成自然语言报告
不开发邮件 Recap 解析模块
不开发聊天记录行情提取模块
15. Agent 最终目标

Agent 每天不仅要回答：

今天 Capesize 市场发生了什么？

还必须回答：

哪些变化会真正影响未来1—15天的Capesize市场？

这些信息是否可信？

现货、货盘和中国需求是否相互验证？

市场是否已经完成定价？

下一步最需要观察什么？
