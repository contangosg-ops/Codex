# Capesize C5 TCE Calculator

A Streamlit web application for calculating a single Capesize C5 voyage TCE using the Baltic non-scrubber BCI 182 Type vessel description.

## Scope

This first version is intentionally focused on one workflow:

- Vessel: Baltic BCI 182 Type
- Route: C5 Qingdao-Dampier-Qingdao round voyage
- Ballast leg: Qingdao to Dampier
- Laden leg: Dampier to Qingdao
- Distance basis: 3,532 nm each way from Netpas
- Sea margin: 5%
- Load rate: 80,000 mt/day
- Discharge rate: 30,000 mt/day
- Dampier load port cost: USD 140,000
- Qingdao discharge port cost: USD 120,000
- Cargo basis: 160,000 mt
- Speed and consumption: automatically optimized across 16 ballast/laden speed combinations
- Output: TCE USD/day and voyage economics breakdown

## Features

- Fixed Baltic BCI 182 Type vessel specification.
- Non-scrubber fitted vessel, 182,000 mt DWT on 18.2 m SSW draft, max age 10 years.
- LOA 292 m, beam 45 m, TPC 123, 199,500 cbm grain.
- Speed and consumption table:
  - 14 knots: 52 mt/day laden, 44 mt/day ballast MFO
  - 13 knots: 44 mt/day laden, 36 mt/day ballast MFO
  - 12 knots: 36 mt/day laden, 29 mt/day ballast MFO
  - 11 knots: 29 mt/day laden, 23 mt/day ballast MFO
- No diesel at sea.
- Automatically calculate all 16 ballast/laden speed and consumption combinations and select the combination with the highest TCE.
- Input C5 freight rate, commission, HSFO price, VLSFO price, port time, waiting time, port cost, canal cost, and other cost.
- Use HSFO for scrubber fitted vessels and VLSFO for non-scrubber fitted vessels. If scrubber status is missing, default to non-scrubber fitted.
- Apply sea margin to ballast and laden sea days before calculating total voyage days and sea bunker cost.
- Calculate load port days and discharge port days from cargo quantity and handling rates.
- Split port costs into Dampier load port cost and Qingdao discharge port cost.
- Calculate Gross Freight, Commission, Net Freight, voyage days, bunker cost, total voyage cost, net voyage profit, and TCE USD/day.
- Export the C5 TCE result to Excel.

## Project Structure

```text
.
+-- app.py
+-- modules
|   +-- tce_calculator.py
|   +-- excel_exporter.py
+-- data
|   +-- vessels.csv
|   +-- routes.csv
+-- requirements.txt
+-- README.md
```

## Core Formula

```text
TCE = Net Voyage Profit / Total Voyage Days

Gross Freight = Cargo Quantity x Freight Rate
Net Freight = Gross Freight x (1 - Commission %)
Total Voyage Days = Ballast Days + Laden Days + Load Port Days + Discharge Port Days + Waiting Days
Load Port Days = Cargo Quantity / Load Rate
Discharge Port Days = Cargo Quantity / Discharge Rate
Ballast Days Base = Ballast Distance / Ballast Speed / 24
Laden Days Base = Laden Distance / Laden Speed / 24
Ballast Days = Ballast Days Base x (1 + Sea Margin %)
Laden Days = Laden Days Base x (1 + Sea Margin %)
Bunker Cost = Sea Bunker Cost + Port Bunker Cost
Net Voyage Profit = Net Freight - Bunker Cost - Port Cost - Canal Cost - Other Cost
Port Cost = Load Port Cost + Discharge Port Cost
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit in your browser.
