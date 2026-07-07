# Codex Operations Tools

This repository contains internal shipping-market tools used by Contango SG operations.

## Capesize C5 TCE Calculator

A Streamlit web application for calculating a single Capesize C5 voyage TCE using the Baltic non-scrubber BCI 182 Type vessel description.

### Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## FFA Reporting Scripts

The FFA workflow builds Excel reports for open interest, SGX NLT trades, and EEX trade tape data.

Main scripts:

- `create_open_interest_report.py`: builds the open interest report.
- `add_sgx_nlt_to_report.py`: adds SGX and EEX trade summaries and charts.
- `gmail_connect.py`: authenticates Gmail read-only access for attachment retrieval.
- `connect_gmail.ps1`: helper for Gmail setup on Windows.

Local-only files are intentionally ignored and should not be committed:

- `credentials.json`
- `token.json`
- `attachments/`
- generated `*.xlsx` reports
- generated `sgx_nlt_*.csv` source files

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the report workflow:

```powershell
python .\create_open_interest_report.py
python .\add_sgx_nlt_to_report.py
```
