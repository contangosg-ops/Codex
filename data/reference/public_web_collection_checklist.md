# 公开网络信息收集清单

## 可用范围

可以检索网上公开信息，用于补充 Capesize 每日市场判断。

## 优先顺序

1. 官方和原始来源：Baltic Exchange、港口、海关、政府、交易所、清算所、上市公司、矿山公司。
2. 可信行业媒体和数据机构：Reuters、Bloomberg、Fastmarkets、Argus、Mysteel、S&P Global、TradeWinds、Lloyd's List、Splash247。
3. 行业评论和公开观点：只能作为辅助信息，不能单独形成核心结论。

## 每条信息必须记录

- `published_at`
- `event_date`
- `title`
- `summary`
- `region`
- `affected_market`
- `impact_direction`
- `impact_horizon`
- `impact_strength`
- `confidence`
- `source`
- `source_url`
- `verified`

## 禁止

- 不使用 FFA Recap 邮件。
- 不使用经纪商 Recap 邮件作为核心来源。
- 不把聊天记录、转述报价或未验证 OTC 成交当成正式市场数据。
- 不用没有明确日期的信息解释当前市场。
- 不输出没有来源的精确数字。
