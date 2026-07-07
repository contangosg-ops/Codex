# Capesize 信息收集系统

这个文件夹是一套本地 Capesize 日报整理系统，用来把每日收集到的公开信息整理为结构化数据，并生成 Word 日报。报告只做信息整理、影响归类和数据质量说明，不提供交易建议。

## 日常使用

1. 在 `data/raw/` 填写当天的数据文件，文件名使用日期：
   - `spot_YYYY-MM-DD.csv`
   - `ffa_public_YYYY-MM-DD.csv`
   - `cargo_YYYY-MM-DD.csv`
   - `china_demand_YYYY-MM-DD.csv`
   - `pilbara_shipments_YYYY-MM-DD.csv`
   - `mine_company_news_YYYY-MM-DD.csv`
   - `research_summaries_YYYY-MM-DD.csv`
   - `weather_YYYY-MM-DD.csv`
   - `commodity_prices_YYYY-MM-DD.csv`
   - `bunker_prices_YYYY-MM-DD.csv`
   - `news_YYYY-MM-DD.json`
2. 运行生成脚本：

```powershell
.\src\reports\New-CapeDailyReport.ps1
```

3. Word 报告会保存到：

```text
reports/daily/cape_daily_report_YYYY-MM-DD.docx
```

## 数据原则

- 可以检索网上公开信息，但必须使用公开、合法、可验证来源。
- 不虚构价格、成交量、货盘或发运量。
- 缺失数据保持为空。
- 每条数据必须保留 `source`、`source_url` 和 `collected_at`。
- 发布日期和事件日期分开记录。
- 未验证信息必须标记为 `verified = false` 或在报告中写明“未验证”。
- 不读取、不解析、不依赖 FFA Recap 邮件、经纪商 Recap、聊天记录报价或未验证场外交易。

## 公开信息检索范围

优先检索：

- Baltic Exchange、交易所、清算所、港口、海关、政府部门等官方来源
- 矿山公司、上市公司公告、财报、生产报告
- Reuters、Bloomberg、Fastmarkets、Argus、Mysteel、S&P Global、TradeWinds、Lloyd's List、Splash247 等可信行业来源

检索后需要记录：

- 信息发布时间
- 事件发生时间
- 来源名称
- 来源链接
- 采集时间
- 是否已验证
- 对 Capesize 的影响方向、影响周期和置信度

## 报告内容范围

日报按以下模块做客观整理：

1. Spot Market
2. Public FFA Market Data
3. Research Summaries
4. Mine and Company Updates
5. Pilbara Daily Shipments
6. Cargo Demand
7. China Demand
8. Weather
9. Commodity Prices
10. Bunker Prices
11. Related Industry News
12. Data Quality

报告输出不包含交易建议、操作方向、建仓/平仓建议、具体交易执行建议或主观投资判断。

## 重点跟踪对象

矿山新闻及动态：

- 铁矿：BHP、Vale、FMG、Rio Tinto、Roy Hill、CSN、Anglo American、西芒杜相关项目
- 铝矾土：几内亚、澳洲、巴西及其他主要铝矾土矿山和出口项目

中国需求：

- 高炉开工率
- 铁水产量
- 钢厂利润
- 港口库存
- 铁矿库存

天气：

- 澳洲主要铁矿出口港和矿区
- 巴西主要铁矿出口港和矿区
- 几内亚铝矾土相关港口和矿区
- 中国主要铁矿接卸港口

价格：

- 铁矿石
- 铝矾土
- 动力煤
- 焦煤
- 氧化铝
- 新加坡、舟山、鹿特丹高低硫燃油

## 文件夹说明

- `data/raw/`：每日原始录入数据
- `data/processed/`：清洗后数据
- `data/reference/`：模板和参考表
- `reports/daily/`：每日 Word 报告
- `reports/weekly/`：周报
- `src/reports/`：报告生成脚本
- `src/`：后续采集、解析和报告脚本
- `config/`：来源、字段和报告配置
- `logs/`：运行日志
