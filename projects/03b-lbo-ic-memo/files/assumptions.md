# DXP LBO assumptions

- USD millions except price, percentages and multiples. Source data through fiscal 2025 with the November 23, 2026 quote and November 2 share count. The mixed-date snapshot is an explicit simplification.
- The FY23 10-K supplies point-in-time FY23 balances omitted from the FY25/22 balance sheet dates. FY21–FY25 operating history spans the requested filings.
- The premium applies to equity value. Debt payoff and cash offset bridge to enterprise value. Debt uses carrying amounts. The simplified model excludes closing debt reconciliation, preferred shares, finance lease liabilities, transaction tax and NOLs.
- The sponsor cash flow occurs at closing and at year five. The closed-form return is independently computed in Python and compared to spreadsheet IRR.
- The downside holds margins 200 bps below base from year two forward. Covenants and all financing terms are hypothetical. No revolver is modeled.
- Independent normalizations and market data references are recorded in historical-data.csv.

## Build verification

- Opened public pages beyond search excerpts. Raw GitHub download verified across seven Olist tables. Python, pandas, SQLite, SciPy and openpyxl verified. XLSX, DOCX, PPTX, PDF and HTML generation verified. SciPy supplied the logistic regression.
- Recalculated lbo-model.xlsx in LibreOffice and checked cached values. 296 formulas, 0 error cells.
