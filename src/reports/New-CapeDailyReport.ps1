param(
    [string]$Date = (Get-Date).ToString("yyyy-MM-dd")
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$rawDir = Join-Path $root "data\raw"
$reportDir = Join-Path $root "reports\daily"
$logDir = Join-Path $root "logs"
$null = New-Item -ItemType Directory -Force -Path $rawDir, $reportDir, $logDir

function Read-CsvIfExists {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        return @(Import-Csv -LiteralPath $Path -Encoding UTF8)
    }
    return @()
}

function Read-JsonIfExists {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        $content = Get-Content -Raw -LiteralPath $Path -Encoding UTF8
        if ([string]::IsNullOrWhiteSpace($content)) { return @() }
        return @($content | ConvertFrom-Json)
    }
    return @()
}

function Escape-XmlText {
    param([AllowNull()][string]$Text)
    if ($null -eq $Text -or $Text -eq "") { return "" }
    return [System.Security.SecurityElement]::Escape($Text)
}

function Add-Para {
    param(
        [System.Collections.Generic.List[string]]$Parts,
        [string]$Text,
        [bool]$Bold = $false,
        [string]$Style = ""
    )
    $escaped = Escape-XmlText $Text
    $styleXml = ""
    if ($Style) { $styleXml = "<w:pPr><w:pStyle w:val=""$Style""/></w:pPr>" }
    $boldXml = ""
    if ($Bold) { $boldXml = "<w:rPr><w:b/></w:rPr>" }
    $Parts.Add("<w:p>$styleXml<w:r>$boldXml<w:t xml:space=""preserve"">$escaped</w:t></w:r></w:p>")
}

function Add-Section {
    param([System.Collections.Generic.List[string]]$Parts, [string]$Title)
    Add-Para -Parts $Parts -Text $Title -Bold $true -Style "Heading1"
}

function Add-Line {
    param([System.Collections.Generic.List[string]]$Parts, [string]$Text)
    Add-Para -Parts $Parts -Text $Text
}

function New-Docx {
    param(
        [string]$OutputPath,
        [System.Collections.Generic.List[string]]$BodyParts
    )

    $temp = Join-Path ([System.IO.Path]::GetTempPath()) ("cape_docx_" + [System.Guid]::NewGuid().ToString("N"))
    $wordDir = Join-Path $temp "word"
    $relsDir = Join-Path $temp "_rels"
    $null = New-Item -ItemType Directory -Force -Path $wordDir, $relsDir

    $contentTypes = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
'@
    $rels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
'@
    $styles = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Microsoft YaHei"/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="38"/></w:rPr></w:style>
</w:styles>
'@
    $body = [string]::Join("", $BodyParts)
    $document = "<?xml version=""1.0"" encoding=""UTF-8"" standalone=""yes""?><w:document xmlns:w=""http://schemas.openxmlformats.org/wordprocessingml/2006/main""><w:body>$body<w:sectPr><w:pgSz w:w=""11906"" w:h=""16838""/><w:pgMar w:top=""1440"" w:right=""1440"" w:bottom=""1440"" w:left=""1440""/></w:sectPr></w:body></w:document>"

    Set-Content -LiteralPath (Join-Path $temp "[Content_Types].xml") -Value $contentTypes -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $relsDir ".rels") -Value $rels -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $wordDir "styles.xml") -Value $styles -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $wordDir "document.xml") -Value $document -Encoding UTF8

    if (Test-Path -LiteralPath $OutputPath) { Remove-Item -LiteralPath $OutputPath -Force }
    $zipPath = [System.IO.Path]::ChangeExtension($OutputPath, ".zip")
    if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
    Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $zipPath -Force
    Move-Item -LiteralPath $zipPath -Destination $OutputPath -Force
    Remove-Item -LiteralPath $temp -Recurse -Force
}

$pilbaraShipments = Read-CsvIfExists (Join-Path $rawDir "pilbara_shipments_$Date.csv")
$commodityPrices = Read-CsvIfExists (Join-Path $rawDir "commodity_prices_$Date.csv")
$sgxFutures = Read-CsvIfExists (Join-Path $rawDir "sgx_futures_$Date.csv")
$bunkerPrices = Read-CsvIfExists (Join-Path $rawDir "bunker_prices_$Date.csv")
$mineCompanyNews = Read-CsvIfExists (Join-Path $rawDir "mine_company_news_$Date.csv")
$researchSummaries = Read-CsvIfExists (Join-Path $rawDir "research_summaries_$Date.csv")
$news = Read-JsonIfExists (Join-Path $rawDir "news_$Date.json")
$reportDate = [datetime]::ParseExact($Date, "yyyy-MM-dd", [System.Globalization.CultureInfo]::InvariantCulture)

$parts = [System.Collections.Generic.List[string]]::new()
Add-Para -Parts $parts -Text "Capesize Daily Information Report - $Date" -Bold $true -Style "Title"
Add-Para -Parts $parts -Text ("生成时间：" + (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz"))
Add-Para -Parts $parts -Text "说明：本日报只做公开信息和数据摘要，不包含市场判断、评分或交易建议。"

Add-Section -Parts $parts -Title "今日数据摘要"

$ironOreRow = $pilbaraShipments | Where-Object { $_.commodity -eq "Iron Ore" -and $_.shipment_volume_tonnes } | Select-Object -First 1
if ($ironOreRow) {
    Add-Line -Parts $parts -Text ("Port Hedland 铁矿石装港：{0} 吨" -f $ironOreRow.shipment_volume_tonnes)
}

$totalCargoRow = $pilbaraShipments | Where-Object { $_.commodity -eq "All loaded cargo" -and $_.shipment_volume_tonnes } | Select-Object -First 1
if ($totalCargoRow) {
    Add-Line -Parts $parts -Text ("Port Hedland 全部装港货物：{0} 吨" -f $totalCargoRow.shipment_volume_tonnes)
}

$shipScheduleRows = @($pilbaraShipments | Where-Object { $_.terminal -eq "Shipping program" -and $_.vessel_count })
if ($shipScheduleRows.Count -gt 0) {
    $items = @()
    foreach ($row in $shipScheduleRows) { $items += ("{0}: {1} 艘" -f $row.date, $row.vessel_count) }
    Add-Line -Parts $parts -Text ("Port Hedland 船期（Pilbara Ports 当前公开 PDF：As of JUL 1 2026 10:24PM，公开可见范围截至 2026-07-03）：" + [string]::Join("、", $items))
}

$ironOreFutures = $commodityPrices | Where-Object { $_.commodity -eq "铁矿石" -and $_.price } | Select-Object -First 1
if ($ironOreFutures) { Add-Line -Parts $parts -Text ("铁矿石主力期货：{0} {1}/{2}，较前一日 {3}（{4}）" -f $ironOreFutures.price, $ironOreFutures.currency, $ironOreFutures.unit, $ironOreFutures.daily_change, $ironOreFutures.daily_change_pct) }

$cokingCoalFutures = $commodityPrices | Where-Object { $_.commodity -eq "焦煤" -and $_.price } | Select-Object -First 1
if ($cokingCoalFutures) { Add-Line -Parts $parts -Text ("焦煤主力期货：{0} {1}/{2}，较前一日 {3}（{4}）" -f $cokingCoalFutures.price, $cokingCoalFutures.currency, $cokingCoalFutures.unit, $cokingCoalFutures.daily_change, $cokingCoalFutures.daily_change_pct) }

$aluminaFutures = $commodityPrices | Where-Object { $_.commodity -eq "氧化铝" -and $_.price } | Select-Object -First 1
if ($aluminaFutures) { Add-Line -Parts $parts -Text ("氧化铝主力期货：{0} {1}/{2}，较前一日 {3}（{4}）" -f $aluminaFutures.price, $aluminaFutures.currency, $aluminaFutures.unit, $aluminaFutures.daily_change, $aluminaFutures.daily_change_pct) }

$sgxIronOre = $sgxFutures | Where-Object { $_.contract_code -like "FEF*" -and $_.last_price } | Select-Object -First 1
if ($sgxIronOre) { Add-Line -Parts $parts -Text ("新加坡新交所铁矿石美元期货：{0} {1}/{2}，合约 {3}，较前一日 {4}（{5}）" -f $sgxIronOre.last_price, $sgxIronOre.currency, $sgxIronOre.unit, $sgxIronOre.contract_code, $sgxIronOre.daily_change, $sgxIronOre.daily_change_pct) }

$sgVlsfo = $bunkerPrices | Where-Object { $_.port -eq "Singapore" -and $_.fuel_grade -eq "VLSFO" -and $_.price_usd_per_tonne } | Select-Object -First 1
if ($sgVlsfo) { Add-Line -Parts $parts -Text ("新加坡 VLSFO：{0} 美元/吨，较前一日 {1}" -f $sgVlsfo.price_usd_per_tonne, $sgVlsfo.daily_change) }

$sgIfo = $bunkerPrices | Where-Object { $_.port -eq "Singapore" -and $_.fuel_grade -eq "IFO380" -and $_.price_usd_per_tonne } | Select-Object -First 1
if ($sgIfo) { Add-Line -Parts $parts -Text ("新加坡 IFO380：{0} 美元/吨，较前一日 {1}" -f $sgIfo.price_usd_per_tonne, $sgIfo.daily_change) }

$rtmVlsfo = $bunkerPrices | Where-Object { $_.port -eq "Rotterdam" -and $_.fuel_grade -eq "VLSFO" -and $_.price_usd_per_tonne } | Select-Object -First 1
if ($rtmVlsfo) { Add-Line -Parts $parts -Text ("鹿特丹 VLSFO：{0} 美元/吨，较前一日 {1}" -f $rtmVlsfo.price_usd_per_tonne, $rtmVlsfo.daily_change) }

$zhoushanMissing = $bunkerPrices | Where-Object { $_.port -eq "Zhoushan" -and -not $_.price_usd_per_tonne } | Select-Object -First 1
if ($zhoushanMissing) { Add-Line -Parts $parts -Text "舟山燃油：公开页面需要登录/订阅，未录入数值" }

$missingCommodityNames = @($commodityPrices | Where-Object { -not $_.price -and $_.commodity } | ForEach-Object { $_.commodity })
if ($missingCommodityNames.Count -gt 0) {
    Add-Line -Parts $parts -Text ("未取得公开可验证价格：" + [string]::Join("、", $missingCommodityNames))
}

Add-Section -Parts $parts -Title "新闻和研报摘要"
$recentItems = @()
foreach ($row in $mineCompanyNews) {
    $publishedAt = [datetime]::MinValue
    if ([datetime]::TryParse([string]$row.published_at, [ref]$publishedAt)) {
        if (($reportDate - $publishedAt).TotalDays -le 2 -and ($reportDate - $publishedAt).TotalDays -ge 0) {
            $recentItems += [PSCustomObject]@{
                Key = (($row.company + "|" + $row.asset_or_project + "|" + $row.title) -replace "Goldman Sachs|Fortescue downgrade reported by media|媒体报道 Goldman Sachs 下调 Fortescue 评级", "Fortescue-GoldmanSachs")
                Date = $row.published_at
                Label = $row.company
                Text = $row.summary
                Source = $row.source
            }
        }
    }
}
foreach ($row in $researchSummaries) {
    $publishedAt = [datetime]::MinValue
    if ([datetime]::TryParse([string]$row.published_at, [ref]$publishedAt)) {
        if (($reportDate - $publishedAt).TotalDays -le 2 -and ($reportDate - $publishedAt).TotalDays -ge 0) {
            $recentItems += [PSCustomObject]@{
                Key = (($row.institution + "|" + $row.title + "|" + $row.mentioned_companies) -replace "Goldman Sachs|Fortescue downgrade reported by media|媒体报道 Goldman Sachs 下调 Fortescue 评级", "Fortescue-GoldmanSachs")
                Date = $row.published_at
                Label = $row.institution
                Text = $row.key_points
                Source = $row.source
            }
        }
    }
}
$seen = @{}
$writtenNews = 0
foreach ($item in @($recentItems | Sort-Object Date -Descending)) {
    if (-not $item.Text) { continue }
    if ($seen.ContainsKey($item.Key)) { continue }
    $seen[$item.Key] = $true
    Add-Line -Parts $parts -Text ("{0}（{1}）：{2} 来源：{3}。" -f $item.Label, $item.Date, $item.Text, $item.Source)
    $writtenNews += 1
}
if ($writtenNews -eq 0) {
    Add-Line -Parts $parts -Text "最近 2 天未收集到新的矿山、公司或研报摘要。"
}

Add-Section -Parts $parts -Title "缺失数据"
Add-Line -Parts $parts -Text "Capesize 现货精确指数/航线报价：本轮未取得公开可验证精确值"
Add-Line -Parts $parts -Text "公开 FFA 精确数据：本轮未取得公开可验证精确值"
Add-Line -Parts $parts -Text "中国需求精确数据：本轮未取得公开可验证精确值"
Add-Line -Parts $parts -Text "主要港口当前天气精确数据：本轮未取得公开可验证精确值"

Add-Section -Parts $parts -Title "来源说明"
Add-Line -Parts $parts -Text "Pilbara Ports：Port Hedland 月度统计和 shipping program。"
Add-Line -Parts $parts -Text "Sina Futures：铁矿石、焦煤、氧化铝主力连续期货公开行情。"
Add-Line -Parts $parts -Text "SGX：新交所铁矿石美元期货延迟行情。"
Add-Line -Parts $parts -Text "Ship & Bunker：新加坡、鹿特丹燃油价格；舟山页面需要登录/订阅。"
foreach ($item in $news) {
    $publishedAt = [datetime]::MinValue
    if (-not [datetime]::TryParse([string]$item.published_at, [ref]$publishedAt)) { continue }
    if (($reportDate - $publishedAt).TotalDays -gt 2 -or ($reportDate - $publishedAt).TotalDays -lt 0) { continue }
    if ($item.title -and $item.source) {
        Add-Line -Parts $parts -Text ("{0}：{1}" -f $item.source, $item.title)
    }
}

$output = Join-Path $reportDir "cape_daily_report_$Date.docx"
New-Docx -OutputPath $output -BodyParts $parts
Add-Content -LiteralPath (Join-Path $logDir "report_generation.log") -Value ("[" + (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz") + "] Generated clean summary report: " + $output) -Encoding UTF8
Write-Output $output







