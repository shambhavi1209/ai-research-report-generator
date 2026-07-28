"""
llm/extract.py — AI extraction layer.

Sends the source document text to Gemini with a structured-output schema
(the Pydantic ResearchReport from schema.py) and returns a validated object.

Hallucination guardrails (deliberate design decisions):
  1. The prompt instructs the model to return null for anything not present
     in the document — never estimate, and NEVER invent a rating or target price.
  2. response_schema forces valid JSON matching schema.py, so nothing outside
     the schema can leak into the report.
  3. Temperature is kept low (0.2) for deterministic extraction.
"""
from __future__ import annotations

import re

from schema import ResearchReport

MODEL = "gemini-3.5-flash"
MAX_CHARS = 400_000  # ample for Gemini's context; guard against pathological inputs

_FIN_KEYWORDS = re.compile(
    r"revenue|sales|ebitda|profit|pat |margin|crore|₹|rs\.|lakh|eps|balance sheet|"
    r"cash flow|income statement|guidance|order book|shareholding|dividend|quarter|fy2",
    re.IGNORECASE,
)

PROMPT = """You are a meticulous equity-research data extractor. From the source document
below, extract data to fill an equity research report template for the company "{company}".

STRICT RULES — read carefully:
1. Use ONLY facts stated in the document. If a value is not present, return null for it.
2. NEVER estimate, infer, or invent numbers. In particular: `rating` and `target_price`
   must be null unless the document explicitly states a recommendation / target price.
3. Monetary amounts (revenue, EBITDA, PAT, market cap) must be in INR crore. If the
   document states amounts in ₹ million, divide by 10; in ₹ lakh, divide by 100. If the
   currency or unit is unclear, return null rather than guess.
4. `financials`: up to 5 fiscal periods, oldest first. Label actuals with 'A' and any
   estimates the DOCUMENT itself provides with 'E' (e.g. FY25A, FY26E).
5. `investment_highlights`: 3–6 concise analyst-style bullets, each grounded in a specific
   fact from the document (include the numbers).
6. `company_description`: 2–3 factual sentences.
7. `outlook_valuation`: a short paragraph summarising the document's own stated outlook or
   guidance. Do not add your own price predictions or recommendations.

SOURCE DOCUMENT:
----------------
{document}
----------------
Return the extracted data as JSON matching the provided schema."""


def _shrink(text: str, limit: int = MAX_CHARS) -> str:
    """For very long documents, keep the paragraphs densest in financial keywords
    (order preserved) until under the limit. Simple, fast, explainable."""
    if len(text) <= limit:
        return text
    paras = text.split("\n\n")
    scored = sorted(
        range(len(paras)),
        key=lambda i: len(_FIN_KEYWORDS.findall(paras[i])) / (len(paras[i]) + 1),
        reverse=True,
    )
    keep, total = set(), 0
    for i in scored:
        if total + len(paras[i]) > limit:
            continue
        keep.add(i)
        total += len(paras[i])
    return "\n\n".join(paras[i] for i in sorted(keep))


def extract_report(document_text: str, company_name: str, api_key: str) -> ResearchReport:
    from google import genai  # imported lazily so demo mode needs no key/SDK

    client = genai.Client(api_key=api_key)
    prompt = PROMPT.format(company=company_name, document=_shrink(document_text))
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResearchReport,
            temperature=0.2,
        ),
    )
    report: ResearchReport | None = resp.parsed
    if report is None:  # fallback if SDK returns raw text
        report = ResearchReport.model_validate_json(resp.text)
    # The user-typed company name wins over whatever the model read
    if company_name.strip():
        report.company_name = company_name.strip()
    return report
