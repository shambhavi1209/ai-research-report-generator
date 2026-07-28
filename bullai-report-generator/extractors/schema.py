"""
schema.py — Single source of truth for every field in the research report template.
Modeled on the Geojit "Retail Equity Research" sample (Eternal Ltd., Q1FY26).

Every extracted field is Optional with a None default: if the LLM cannot find a
value in the source document it returns null and the template renders "-".
To add a field: (1) add it here with a description (the description doubles as the
LLM instruction), (2) reference it in templates/report.html.
"""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class CompanyData(BaseModel):
    """Sidebar 'Company Data' box + header price block."""
    cmp: Optional[float] = Field(None, description="Current market price per share in Rs, only if stated")
    target_price: Optional[float] = Field(None, description="Analyst target price in Rs, ONLY if explicitly stated in the document. Never estimate.")
    market_cap_cr: Optional[float] = Field(None, description="Market capitalisation in Rs crore")
    week52_high: Optional[float] = Field(None, description="52-week high share price in Rs")
    week52_low: Optional[float] = Field(None, description="52-week low share price in Rs")
    enterprise_value_cr: Optional[float] = Field(None, description="Enterprise value in Rs crore")
    outstanding_shares_cr: Optional[float] = Field(None, description="Outstanding shares in crore")
    free_float_pct: Optional[float] = Field(None, description="Free float %")
    dividend_yield_pct: Optional[float] = None
    beta: Optional[float] = None
    face_value: Optional[float] = Field(None, description="Face value per share in Rs")
    nse_code: Optional[str] = None
    bse_code: Optional[str] = None
    bloomberg_code: Optional[str] = None
    stock_type: Optional[str] = Field(None, description="Market-cap class if stated, e.g. 'Large Cap'")


class Shareholding(BaseModel):
    """Sidebar 'Shareholding (%)' box, latest available period."""
    period: Optional[str] = Field(None, description="Label of the period, e.g. 'Q2FY26'")
    promoters_pct: Optional[float] = None
    fii_pct: Optional[float] = None
    mf_institutions_pct: Optional[float] = Field(None, description="MFs / domestic institutions %")
    public_pct: Optional[float] = None
    others_pct: Optional[float] = None


class PricePerformance(BaseModel):
    """Sidebar 'Price Performance' box — absolute returns %."""
    m3_pct: Optional[float] = None
    m6_pct: Optional[float] = None
    y1_pct: Optional[float] = None


class YearlyFinancials(BaseModel):
    """One column of the annual financials tables. Amounts in Rs crore."""
    period: str = Field(..., description="Fiscal period label, e.g. 'FY25A', 'FY26E' — 'E' only if the document itself provides estimates")
    sales_cr: Optional[float] = Field(None, description="Total revenue / sales in Rs crore")
    growth_pct: Optional[float] = Field(None, description="YoY sales growth %")
    ebitda_cr: Optional[float] = None
    ebitda_margin_pct: Optional[float] = None
    adj_pat_cr: Optional[float] = Field(None, description="Adjusted PAT in Rs crore")
    pat_growth_pct: Optional[float] = None
    eps: Optional[float] = Field(None, description="Adjusted EPS in Rs")
    pe: Optional[float] = Field(None, description="P/E (x)")
    pb: Optional[float] = Field(None, description="P/B (x)")
    ev_ebitda: Optional[float] = Field(None, description="EV/EBITDA (x)")
    roe_pct: Optional[float] = None
    de: Optional[float] = Field(None, description="Debt/Equity (x)")


class QuarterlyRow(BaseModel):
    """One quarter, oldest first in the list. Amounts in Rs crore."""
    period: str = Field(..., description="Quarter label, e.g. 'Q2FY26'")
    sales_cr: Optional[float] = None
    ebitda_cr: Optional[float] = None
    ebitda_margin_pct: Optional[float] = None
    adj_pat_cr: Optional[float] = None
    eps: Optional[float] = Field(None, description="EPS for the quarter in Rs")


class ResearchReport(BaseModel):
    """Top-level object that fills the whole template."""
    company_name: str
    sector: Optional[str] = None
    report_type: Optional[str] = Field("Company Report", description="e.g. 'Q2FY26 Result Update', 'Company Update'")
    report_date: str = Field(default_factory=lambda: date.today().strftime("%d %B, %Y"))
    rating: Optional[str] = Field(None, description="BUY / ACCUMULATE / HOLD / REDUCE / SELL, ONLY if the document states a recommendation. Never invent one.")
    headline: Optional[str] = Field(None, description="One-line report headline summarising the thesis, e.g. 'Blinkit propels growth; valuation limits upside'")
    company_description: Optional[str] = Field(None, description="2-3 factual sentences describing the company and its businesses")
    result_highlights: List[str] = Field(default_factory=list, description="4-6 concise bullets with the key reported numbers (revenue, margins, PAT, growth), each grounded in the document")
    analysis_points: List[str] = Field(default_factory=list, description="2-5 longer 'key highlights' bullets: management commentary, guidance, segment detail — grounded strictly in the document")
    outlook_valuation: Optional[str] = Field(None, description="Paragraph summarising the document's own stated outlook/guidance. No invented price targets or recommendations.")
    company_data: CompanyData = Field(default_factory=CompanyData)
    shareholding: Optional[Shareholding] = None
    price_performance: Optional[PricePerformance] = None
    financials: List[YearlyFinancials] = Field(default_factory=list, description="Up to 5 fiscal years, oldest first")
    quarterly: List[QuarterlyRow] = Field(default_factory=list, description="Up to 5 recent quarters, oldest first")

    @property
    def upside_pct(self) -> Optional[float]:
        cd = self.company_data
        if cd.cmp and cd.target_price and cd.cmp > 0:
            return (cd.target_price - cd.cmp) / cd.cmp * 100.0
        return None
