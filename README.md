# Andrew’s portfolio

Six case studies covering investing, analytics, strategy, product, and operations. Open [the homepage](index.html) to browse the portfolio.

| Project | Result | Main file |
|---|---|---|
| [Hyperbolic – VC investment memo](projects/03a-vc-investment-memo/index.html) | Pass until repeat usage and contribution margin support the GPU marketplace thesis. | [PDF](projects/03a-vc-investment-memo/files/memo.pdf) |
| [DXP Enterprises – LBO and IC memo](projects/03b-lbo-ic-memo/index.html) | Pass at the modeled premium. The five-year base case returns 7.4% against a 20% hurdle. | [PDF](projects/03b-lbo-ic-memo/files/ic-memo.pdf) |
| [Olist – E-commerce repeat purchase](projects/01-ecommerce-repeat-purchase/index.html) | Late orders scored 2.27 stars versus 4.29 on time. The repeat-purchase gap was inconclusive. | [PDF](projects/01-ecommerce-repeat-purchase/files/memo.pdf) |
| [Costco – Gothenburg market entry](projects/02-market-entry-case/index.html) | Pilot paid demand before committing to a third Swedish warehouse. | [PDF](projects/02-market-entry-case/files/executive-summary.pdf) |
| [Acorns – Product teardown and PRD](projects/04-product-teardown-prd/index.html) | Show investors where a transfer stands and what they can safely do next. | [PDF](projects/04-product-teardown-prd/files/prd.pdf) |
| [Relay – Operating system simulation](projects/05-operating-system-simulation/index.html) | One quarter plan keeps a product launch and office opening on schedule in the simulation. | [PDF](projects/05-operating-system-simulation/files/project-plan.pdf) |

## Publish on GitHub Pages

1. Create a public repository on GitHub. Use `<username>.github.io` for an account site at `https://<username>.github.io/`. A repository named `portfolio` publishes at `https://<username>.github.io/portfolio/`.
2. Extract `portfolio-site.zip`. Upload the files and subfolders **inside** `portfolio/` directly to the repository root, preserving their paths. The root contains `index.html`, `about.html`, `.nojekyll`, `assets/`, and `projects/`. Keep the private interview ZIP outside the repository.
3. With the web uploader, select files in batches of at most 100. GitHub's browser limit is 25 MiB per file. Confirm that the empty `.nojekyll` file appears at the repository root. If a hidden-file filter skipped it, create a root-level `.nojekyll` in GitHub.
4. In **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, and save. When deployment completes, the Pages settings show the live URL.

[GitHub Pages publishing guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) · [Browser upload limits](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

## View or reproduce

- **Locally**. Run `python -m http.server 8000 -d portfolio` from the parent directory and open `http://localhost:8000/`.
- **Hyperbolic**. Open the market map workbook or use the two CSV evidence tables. Update the market-size inputs in Excel to reproduce the arithmetic.
- **DXP**. Open the live workbook in Excel or LibreOffice and use the Inputs tab. The entry/exit sensitivity is live. The growth/leverage sensitivity is labeled as a static model rerun.
- **Olist**. From this repository root run `python -m pip install -r requirements.txt`. Change into `projects/01-ecommerce-repeat-purchase/files` and run `python download_data.py data` and `python analyze.py data`. The script loads SQLite, runs the eight queries, independently checks counts in pandas, and writes summary JSON and CSV tables to `analysis-output/`. Open `notebook.ipynb` in Jupyter from the same directory for a notebook walkthrough. Data: Olist, CC BY-NC-SA 4.0.
- **Costco**. Open the workbook and select scenario 1, 2 or 3 in Inputs cell B2. Recalculate and review Model, Sensitivity, and Checks. The independent Python benchmark row refers to original model inputs.
- **Acorns**. Open the tagged review workbook to reproduce theme counts and RICE. Open the mockup page in a browser to try each interaction.
- **Relay**. Open the workbook to recalculate the scorecard and office budget. Read the facts sheet and the task-plan CSV for scenario inputs, milestone dates, task owners and dependencies.

## Sources and notes

Each case-study page links to its assumptions and public sources. Relay is a labeled simulation. Funding terms and valuations in investment work are hypothetical. The portfolio was checked locally for intact paths and downloadable files.
