"""demo_data.py — Canned reports for demo mode / offline testing. The submitted
example PDFs should be regenerated from the real test docs via the LLM path."""
from schema import (CompanyData, PricePerformance, QuarterlyRow, ResearchReport,
                    Shareholding, YearlyFinancials)


def meridian_auto() -> ResearchReport:
    return ResearchReport(
        company_name="Meridian Auto Components Ltd",
        sector="Auto Ancillaries",
        report_type="Q3FY26 Result Update",
        rating="BUY",
        headline="EV driveline ramp-up powers growth; margins inflect",
        company_description=(
            "Meridian Auto Components is a leading Indian manufacturer of precision "
            "transmission and driveline components, supplying domestic OEMs and export "
            "markets across Europe and North America from six plants, with growing "
            "content per vehicle in the EV drivetrain segment."),
        result_highlights=[
            "Q3FY26 revenue grew 18.4% YoY to Rs. 1,284cr, ahead of industry volume growth of 9%, driven by new EV driveline orders and higher export realisations.",
            "EBITDA margin expanded 140bps YoY to 14.8% on softer raw material costs and operating leverage; management guides for a 15%+ exit margin in FY26.",
            "Order book at Rs. 4,100cr (1.7x TTM revenue) with 32% from EV platforms, providing multi-year revenue visibility.",
            "Net debt/EBITDA improved to 0.6x from 1.1x a year ago; Rs. 350cr capex for the Pune EV line is fully funded through internal accruals.",
            "Exports contributed 41% of revenue; a weaker INR and new EU client wins support further traction in FY27.",
        ],
        analysis_points=[
            "Management indicated the EV driveline order pipeline remains strong, with 32% of the order book now from EV platforms versus 21% a year ago, and expects EV share of revenue to cross 25% by FY28.",
            "The new Pune EV line is on schedule for commissioning in Q2FY27 and is expected to add Rs. 900cr of peak annual capacity.",
            "Raw material tailwinds are expected to persist for at least two quarters; the company has passed through part of the benefit to OEMs under indexation clauses.",
        ],
        outlook_valuation=(
            "Management expects a 16% revenue CAGR over FY25-FY28E led by EV driveline "
            "ramp-up and export wins, with EBITDA margins sustaining above 15% as mix "
            "improves. The document states a BUY rating with a target of Rs. 1,480, "
            "valuing the company at 24x FY27E EPS."),
        company_data=CompanyData(
            cmp=1236, target_price=1480, market_cap_cr=18540, week52_high=1342,
            week52_low=812, enterprise_value_cr=18930, outstanding_shares_cr=15.0,
            free_float_pct=45.8, dividend_yield_pct=0.8, beta=1.1, face_value=2.0,
            nse_code="MERIDAUTO", bse_code="543912", bloomberg_code="MERID:IN",
            stock_type="Mid Cap"),
        shareholding=Shareholding(period="Q3FY26", promoters_pct=54.2, fii_pct=17.6,
                                  mf_institutions_pct=14.9, public_pct=10.1, others_pct=3.2),
        price_performance=PricePerformance(m3_pct=8.2, m6_pct=21.5, y1_pct=42.7),
        financials=[
            YearlyFinancials(period="FY24A", sales_cr=3620, growth_pct=12.1, ebitda_cr=470, ebitda_margin_pct=13.0, adj_pat_cr=252, pat_growth_pct=14.5, eps=33.6, pe=36.8, pb=5.8, ev_ebitda=21.5, roe_pct=15.2, de=0.4),
            YearlyFinancials(period="FY25A", sales_cr=4185, growth_pct=15.6, ebitda_cr=572, ebitda_margin_pct=13.7, adj_pat_cr=308, pat_growth_pct=22.2, eps=41.1, pe=30.1, pb=5.1, ev_ebitda=17.9, roe_pct=16.4, de=0.3),
            YearlyFinancials(period="FY26E", sales_cr=4890, growth_pct=16.8, ebitda_cr=733, ebitda_margin_pct=15.0, adj_pat_cr=398, pat_growth_pct=29.2, eps=53.1, pe=23.3, pb=4.3, ev_ebitda=14.1, roe_pct=18.1, de=0.3),
            YearlyFinancials(period="FY27E", sales_cr=5660, growth_pct=15.7, ebitda_cr=875, ebitda_margin_pct=15.5, adj_pat_cr=478, pat_growth_pct=20.1, eps=63.7, pe=19.4, pb=3.6, ev_ebitda=11.8, roe_pct=18.9, de=0.2),
        ],
        quarterly=[
            QuarterlyRow(period="Q3FY25", sales_cr=1085, ebitda_cr=145, ebitda_margin_pct=13.4, adj_pat_cr=78, eps=5.2),
            QuarterlyRow(period="Q4FY25", sales_cr=1120, ebitda_cr=156, ebitda_margin_pct=13.9, adj_pat_cr=84, eps=5.6),
            QuarterlyRow(period="Q1FY26", sales_cr=1174, ebitda_cr=168, ebitda_margin_pct=14.3, adj_pat_cr=91, eps=6.1),
            QuarterlyRow(period="Q2FY26", sales_cr=1236, ebitda_cr=180, ebitda_margin_pct=14.6, adj_pat_cr=98, eps=6.5),
            QuarterlyRow(period="Q3FY26", sales_cr=1284, ebitda_cr=190, ebitda_margin_pct=14.8, adj_pat_cr=104, eps=6.9),
        ],
    )


def kaveri_foods() -> ResearchReport:
    return ResearchReport(
        company_name="Kaveri Foods Ltd",
        sector="FMCG \u2014 Packaged Foods",
        report_type="Company Update",
        rating=None,  # missing -> NOT RATED
        headline="Quick commerce scales; input costs the key monitorable",
        company_description=(
            "Kaveri Foods is a South-India-focused packaged foods company with leading "
            "positions in ready-to-cook mixes and traditional snacks, distributed through "
            "210,000 retail outlets and a fast-growing quick-commerce channel."),
        result_highlights=[
            "Revenue grew 12.3% in FY25 to Rs. 2,140cr with volume growth of 9% \u2014 among the best in the packaged foods peer set.",
            "Quick-commerce and e-commerce now contribute 11% of sales, up from 6% two years ago, at gross margins ~300bps above general trade.",
            "Gross margin pressure from palm oil and milk inflation was largely offset by pricing; EBITDA margin held at 16.1%.",
            "The company is debt-free with Rs. 410cr of net cash and generated Rs. 238cr of free cash flow in FY25.",
        ],
        analysis_points=[],  # deliberately empty -> section skipped
        outlook_valuation=(
            "Management targets a national rollout of its top three SKUs over FY26-FY27 "
            "and commissioning of the new Hosur plant by Q2FY27. The source document does "
            "not state a rating or target price, so none is presented."),
        company_data=CompanyData(
            cmp=486, target_price=None, market_cap_cr=7020, week52_high=545, week52_low=352,
            enterprise_value_cr=6610, outstanding_shares_cr=14.4, free_float_pct=38.5,
            dividend_yield_pct=1.2, beta=None, face_value=1.0,
            nse_code="KAVERIFOOD", bse_code="544120", bloomberg_code=None, stock_type="Small Cap"),
        shareholding=Shareholding(period="FY25", promoters_pct=61.5, fii_pct=8.4,
                                  mf_institutions_pct=12.2, public_pct=17.9, others_pct=None),
        price_performance=PricePerformance(m3_pct=-3.1, m6_pct=6.8, y1_pct=18.9),
        financials=[
            YearlyFinancials(period="FY23A", sales_cr=1705, growth_pct=10.4, ebitda_cr=262, ebitda_margin_pct=15.4, adj_pat_cr=158, pat_growth_pct=11.0, eps=10.9, pe=44.6, pb=9.2, ev_ebitda=25.2, roe_pct=21.5, de=0.0),
            YearlyFinancials(period="FY24A", sales_cr=1905, growth_pct=11.7, ebitda_cr=301, ebitda_margin_pct=15.8, adj_pat_cr=182, pat_growth_pct=15.2, eps=12.6, pe=38.6, pb=8.4, ev_ebitda=22.0, roe_pct=22.1, de=0.0),
            YearlyFinancials(period="FY25A", sales_cr=2140, growth_pct=12.3, ebitda_cr=345, ebitda_margin_pct=16.1, adj_pat_cr=210, pat_growth_pct=15.4, eps=14.5, pe=33.5, pb=7.6, ev_ebitda=19.2, roe_pct=22.8, de=0.0),
        ],
        quarterly=[],  # deliberately empty -> quarterly table + charts fall back
    )


DEMO_REPORTS = {
    "Meridian Auto Components Ltd": meridian_auto,
    "Kaveri Foods Ltd": kaveri_foods,
}
