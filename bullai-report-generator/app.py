"""
app.py — Streamlit UI.

Inputs : company name + one context document (PDF / CSV / TXT)
Output : one-click download of the generated Geojit-style research report PDF.

Run:  streamlit run app.py
"""
from __future__ import annotations

import os

import streamlit as st

from charts.builders import build_charts
from demo_data import DEMO_REPORTS, meridian_auto
from extractors import SUPPORTED_EXTENSIONS, extract_text
from render import render_pdf

st.set_page_config(page_title="AI Research Report Generator", page_icon="📊", layout="centered")

st.title("📊 AI Research Report Generator")
st.caption("Upload a company's financial context document → download a Geojit-style research report PDF.")

with st.sidebar:
    st.subheader("Settings")
    api_key = st.text_input(
        "Gemini API key", type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Or set the GEMINI_API_KEY environment variable.",
    )
    demo_mode = st.toggle(
        "Demo mode (no API key)", value=not bool(api_key),
        help="Renders the report from built-in sample data so the pipeline can be tested offline.",
    )

company = st.text_input("Company name", placeholder="e.g. Meridian Auto Components Ltd")
uploaded = st.file_uploader(
    f"Context document ({' / '.join(e.upper() for e in SUPPORTED_EXTENSIONS)})",
    type=SUPPORTED_EXTENSIONS,
)

if st.button("Generate report", type="primary", use_container_width=True):
    try:
        if demo_mode:
            report = DEMO_REPORTS.get(company, meridian_auto)()
            if company.strip():
                report.company_name = company.strip()
            st.info("Demo mode: report filled from built-in sample data, not the uploaded file.")
        else:
            if not api_key:
                st.error("Enter a Gemini API key or switch on demo mode.")
                st.stop()
            if not uploaded:
                st.error("Upload a context document first.")
                st.stop()
            if not company.strip():
                st.error("Enter the company name.")
                st.stop()
            with st.spinner("Reading document…"):
                text = extract_text(uploaded.getvalue(), uploaded.name)
            with st.spinner("Extracting financials with Gemini…"):
                from llm.extract import extract_report
                report = extract_report(text, company, api_key)

        with st.spinner("Building charts and rendering PDF…"):
            pdf_bytes = render_pdf(report, build_charts(report))

        st.session_state["pdf"] = pdf_bytes
        st.session_state["pdf_name"] = f"{report.company_name.replace(' ', '_')}_research_report.pdf"
        st.session_state["report_json"] = report.model_dump()
        st.success("Report generated.")
    except Exception as e:
        st.error(f"Generation failed: {e}")

# Download button lives OUTSIDE the generate block so it survives Streamlit reruns
if "pdf" in st.session_state:
    st.download_button(
        "⬇️ Download PDF", st.session_state["pdf"],
        file_name=st.session_state["pdf_name"], mime="application/pdf",
        use_container_width=True,
    )
    with st.expander("Extracted data (JSON)"):
        st.json(st.session_state["report_json"])
