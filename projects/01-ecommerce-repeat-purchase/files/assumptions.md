# Olist assumptions and limits

- Source: Olist, https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce, Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (https://creativecommons.org/licenses/by-nc-sa/4.0/). Public CSV mirror: https://github.com/alexcj10/olist-ecommerce-analytics/tree/main/data. Retrieved 2026-11-24. No raw tables are included. Derived Olist aggregates retain attribution and the same license.
- Customers are grouped by customer_unique_id. Raw orders cover 2016-09-04 through 2018-10-17 with 0 duplicated order IDs and 96,096 unique customer identifiers.
- Repeat means two or more distinct qualifying orders. Canceled and unavailable orders are excluded. Delivery analysis uses delivered orders with usable dates; lateness compares calendar dates.
- Equal 90-day follow-up ends at the last purchase date among orders later marked delivered (2018-08-29). The calendar cohort dashboard separately suppresses future/partial cells.
- Product labels are manually translated across all observed category codes. The original Portuguese codes are retained with their English labels. Category totals use item price excluding freight. Category repeat rates refer to repeat purchasing anywhere on the platform. Customers may appear in several categories.
- Rating averages use one order-level average where multiple reviews exist. Payment amounts are observed sums rather than accounting revenue.
- Orders and repeat customers were recomputed in pandas and SQL. The 90-day two-by-two table also matched. Data audit lists row counts, duplicate rows and column nulls.
- The study is observational, historical, single-platform, and right-censored outside the fixed follow-up sample. Logistic regression is fit with SciPy and adjusts for cohort month and state.

## Build verification

- Opened public pages beyond search excerpts. Raw GitHub download verified across seven Olist tables. Python, pandas, SQLite, SciPy and openpyxl verified. XLSX, DOCX, PPTX, PDF and HTML generation verified. SciPy supplied the logistic regression.
