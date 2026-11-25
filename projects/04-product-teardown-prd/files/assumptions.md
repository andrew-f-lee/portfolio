# Review evidence and limits

- Reviewed 2026-11-24 using public pages and the Apple review feed. Sources: https://www.trustpilot.com/review/acorns.com, https://apps.apple.com/us/app/acorns-save-invest-money/id883324671?platform=iphone&see-all=reviews, https://play.google.com/store/apps/details?id=com.acorns.android&hl=en_US. All dated reviews fall between 2025-11-25 and 2026-11-24. Trustpilot and Google timestamps are converted to Los Angeles dates. Apple timestamps retain the reported local date.
- The final sample has 100 reviews, {'App Store': 34, 'Google Play': 4, 'Trustpilot': 62}. Trustpilot includes organically posted entries and a systematic sample of invited entries across nine pages. The Apple feed contributes up to twelve usable reviews from each of three pages, subject to final exclusions. Google Play supplies four recent reviews from its featured dataset.
- Excluded non-core or low-information rows after collection. Kept generic sentiment under usability only when otherwise in scope. Collection audit is in the workbook. Public sources were uneven. Invitation status is unknown for both app stores.
- Exact tag-set self-consistency after a shuffled 15-review second pass: 13/15 (87%). This is one analyst's self-consistency check. The codes and matching rule are in the workbook. The large usability bucket includes short generic reactions.
- Excerpts are short, with Apple excerpts capped in total across the public page. A blank excerpt cell indicates a link and coded record are available without republishing text. No usernames or raw full-text file is included.
- RICE reach is theme share and is not a market estimate. Impact, confidence, effort, rollout thresholds and mockup details are assumptions. The concept does not use Acorns branding or account data.

## Build verification

- Opened public pages beyond search excerpts. Raw GitHub download verified across seven Olist tables. Python, pandas, SQLite, SciPy and openpyxl verified. XLSX, DOCX, PPTX, PDF and HTML generation verified. SciPy supplied the logistic regression.
- Recalculated tagged-reviews.xlsx in LibreOffice and checked cached values. 20 formulas, 0 error cells.
