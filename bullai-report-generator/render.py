"""
render.py — Fills templates/report.html with a ResearchReport and produces PDF bytes.

Missing-field policy lives in the Jinja filters (None -> em-dash) and in
quarterly_view (growth columns are COMPUTED from extracted values, never asked
of the LLM, and omitted when the quarters needed aren't available).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from schema import ResearchReport

TEMPLATE_DIR = Path(__file__).parent / "templates"


def fmt(value: Optional[float], dec: int = 1) -> str:
    if value is None:
        return "\u2014"
    return f"{value:,.{dec}f}"


def rs(value: Optional[float]) -> str:
    return "\u2014" if value is None else f"Rs. {value:,.0f}"


def signed(value: Optional[float]) -> str:
    return "\u2014" if value is None else f"{value:+.1f}%"


def na(value) -> str:
    return "\u2014" if value in (None, "") else str(value)


def _pct(cur: Optional[float], base: Optional[float]) -> Optional[float]:
    if cur is None or base in (None, 0):
        return None
    return (cur - base) / abs(base) * 100.0


def quarterly_view(report: ResearchReport) -> Optional[dict]:
    """Sample-style table: latest quarter vs year-ago (YoY %) and previous quarter
    (QoQ %). Growth is computed here, not extracted. Margin deltas shown in bps."""
    q = report.quarterly
    if not q:
        return None
    latest, prev = q[-1], (q[-2] if len(q) >= 2 else None)
    yoy = q[-5] if len(q) >= 5 else None

    columns = [latest.period]
    if yoy:
        columns += [yoy.period, "YoY Growth (%)"]
    if prev:
        columns += [prev.period, "QoQ Growth (%)"]

    def growth_cell(cur, base, bps=False):
        if cur is None or base is None:
            return "\u2014"
        if bps:
            return f"{(cur - base) * 100:+.0f}bps"
        g = _pct(cur, base)
        return "\u2014" if g is None else f"{g:.1f}"

    rows = []
    for label, attr, dec, bps in [
        ("Sales", "sales_cr", 0, False),
        ("EBITDA", "ebitda_cr", 0, False),
        ("Margin (%)", "ebitda_margin_pct", 1, True),
        ("Adj PAT", "adj_pat_cr", 0, False),
        ("EPS (Rs)", "eps", 2, False),
    ]:
        cur = getattr(latest, attr)
        if cur is None and not any(getattr(x, attr) is not None for x in q):
            continue
        cells = [fmt(cur, dec)]
        if yoy:
            cells += [fmt(getattr(yoy, attr), dec), growth_cell(cur, getattr(yoy, attr), bps)]
        if prev:
            cells += [fmt(getattr(prev, attr), dec), growth_cell(cur, getattr(prev, attr), bps)]
        rows.append({"label": label, "cells": cells})
    return {"columns": columns, "rows": rows} if rows else None


def _env() -> Environment:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
    env.filters.update({"fmt": fmt, "rs": rs, "signed": signed, "na": na})
    return env


def render_html(report: ResearchReport, charts: dict) -> str:
    css = (TEMPLATE_DIR / "styles.css").read_text()
    return _env().get_template("report.html").render(
        report=report, charts=charts, upside=report.upside_pct,
        qtable=quarterly_view(report), css=css,
    )


def render_pdf(report: ResearchReport, charts: dict) -> bytes:
    return HTML(string=render_html(report, charts), base_url=str(TEMPLATE_DIR)).write_pdf()
