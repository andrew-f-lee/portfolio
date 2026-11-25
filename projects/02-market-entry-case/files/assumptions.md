# Gothenburg market entry assumptions

- Working hypothesis: Working hypothesis: existing Swedish operations make expansion testable, but store economics may be too thin to sign a full warehouse lease now.
- The case extends a real expansion to a hypothetical third Swedish warehouse. The source geography is the entire county and the reachable portion is an assumption, pending drive-time analysis.
- SCB food and beverage retail sales provide a directional ceiling. The model uses a merchandise basket proxy and treats price comparisons as indicative. Year-five bottom-up sales are a captured slice, not all eligible local spend. The workbook also compares captured estimates at the same funnel stage.
- Membership revenue nets out assumed VAT on the public price. Store costs, discount rate and cash tax are modeled assumptions. Cash tax is applied to positive operating contribution as a cash proxy, without tax depreciation or losses.
- The five-year model excludes terminal value, a working capital release, and real estate residual value. Use the NPV as a five-year capital-recovery hurdle and extend it before approving a full-life investment.
- Independent Python NPV computes the discounted cash flows from the scenario inputs. Expected scenarios: Conservative SEK -710.7m, Base SEK -423.3m, Optimistic SEK -146.9m.

## Build verification

- Opened public pages beyond search excerpts. Raw GitHub download verified across seven Olist tables. Python, pandas, SQLite, SciPy and openpyxl verified. XLSX, DOCX, PPTX, PDF and HTML generation verified. SciPy supplied the logistic regression.
- Recalculated market-entry-model.xlsx in LibreOffice and checked cached values. 119 formulas, 0 error cells.
- Changed the selector and recalculated all three copies. Five-year NPVs: -710.72, -423.34, and -146.88 SEK million.
