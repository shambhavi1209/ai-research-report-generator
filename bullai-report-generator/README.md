# AI Research Report Generator

Minimal web app that takes a company's financial context document (PDF / CSV / TXT)
and returns a downloadable, auto-filled **Geojit "Retail Equity Research" report PDF** (teal theme, matched to the provided Eternal Ltd. sample) —
matching the sample's layout: rating header, stock-data sidebar, shareholding,
investment highlights, consolidated financials table, quarterly snapshot, charts,
and outlook narrative.

## How to run

```bash
pip install -r requirements.txt        # WeasyPrint needs pango/cairo: on Ubuntu →
                                       # sudo apt install libpango-1.0-0 libpangocairo-1.0-0
export GEMINI_API_KEY=your_key         # get one at https://aistudio.google.com
streamlit run app.py
```

Then: enter the company name → upload the context document → **Generate report** →
**Download PDF**. Toggle **Demo mode** in the sidebar to run without an API key
(uses built-in sample data so the full pipeline can be tested offline).

Headless CLI (used to produce the examples):

```bash
python generate.py --file sample_inputs/meridian_auto_q3fy26_commentary.txt \
                   --company "Meridian Auto Components Ltd" --out examples/meridian.pdf
```

## Architecture

```
upload (pdf/csv/txt)
   └── extractors/            → plain text (+ tables flattened, financial signal preserved)
         └── llm/extract.py   → Gemini 2.5 Flash, structured output → schema.ResearchReport
               ├── charts/builders.py → matplotlib PNGs (base64)
               └── render.py  → Jinja2 fills templates/report.html → WeasyPrint → PDF
app.py = Streamlit UI · generate.py = headless CLI
```

## Where the template fields are defined

**One file: `schema.py`.** Every field in the PDF is a Pydantic field there; the same
schema is passed to Gemini as its structured-output contract, so the LLM literally
cannot return fields the template doesn't know about.

| schema.py | Template location |
|---|---|
| `rating`, `headline`, `company_data.cmp/target_price` | Header rating block (upside % is computed, never extracted) |
| `company_data.*` | Header strip + sidebar "Company Data" box |
| `shareholding`, `price_performance` | Sidebar boxes |
| `company_description`, `result_highlights` | Main column, page 1; `analysis_points` -> page-2 "Key highlights" |
| `financials[]` | Sidebar "Y.E March" estimates table + page-2 "Consolidated Financials" + annual chart |
| `quarterly[]` | "Quarterly Financials Consolidated" (YoY/QoQ computed in render.py, never extracted) + 2x2 charts |
| `outlook_valuation` | Page-1 "Outlook & Valuation" |

### Adding a new field (3 steps)
1. Add it to the relevant model in `schema.py` (Optional, default None, with a `description` — the description doubles as the LLM instruction).
2. If needed, add a rule about it in `llm/extract.py`'s prompt.
3. Reference it in `templates/report.html` with a formatting filter, e.g. `{{ report.stock_data.beta | fmt(2) }}`.

## Design decisions

- **HTML + Jinja2 + WeasyPrint instead of ReportLab.** The sample is a dense,
  styled, multi-column layout; recreating it declaratively in CSS is faster to build,
  far easier to tweak against the sample, and keeps template and data fully separated.
- **Hallucination guardrails.** The prompt requires `null` for anything not in the
  document; **rating and target price are never invented** (a fabricated target price
  is the worst possible failure in equity research). Structured output pins the JSON
  to the schema; temperature 0.2.
- **Missing fields degrade gracefully.** Every extracted field is `Optional`; Jinja
  filters render `None` as "—", empty sections collapse or show an explicit note
  (see the Kaveri example: NOT RATED, no target, no quarterly section).
- **Long documents.** Inputs beyond ~400k chars are reduced by keeping the paragraphs
  densest in financial keywords (order preserved) — simple, fast, explainable.
- **Modularity.** New input format = one function in `extractors/`. New chart = one
  builder in `charts/builders.py`. New field = the 3 steps above.

## Examples

`examples/` contains two PDFs produced by this pipeline from the docs in
`sample_inputs/` — one full-data case (Meridian, TXT input, BUY + target) and one
sparse-data case (Kaveri, CSV input, no rating/target/quarterly → graceful blanks).

## Limitations / next steps

- Scanned (image-only) PDFs would need an OCR pass (e.g. pytesseract) in `extractors/`.
- Peer-comparison and balance-sheet/cash-flow pages of the sample are not yet templated;
  the schema/section pattern extends to them directly.
- Extracted values are not yet cross-checked against source snippets programmatically;
  a per-field `source_snippet` for click-through verification is the natural next step.
