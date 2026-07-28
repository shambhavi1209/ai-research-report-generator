"""
charts/builders.py — Report charts as base64 PNG data URIs, styled to match the
Geojit sample: teal bars with an orange trend line, laid out in a 2x2 grid.

Each builder returns None when there is not enough data; the grid packer simply
omits the slot — part of graceful missing-field handling.
"""
from __future__ import annotations

import base64
import io
from typing import List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from schema import ResearchReport

TEAL = "#0E7C6F"
ORANGE = "#F5A623"
SLATE = "#21313C"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.edgecolor": "#D8DEE3", "axes.linewidth": 0.8,
})


def _uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight", transparent=True)
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#ECF0F2", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, colors=SLATE, labelsize=7)


def _growth_series(values: List[Optional[float]]) -> List[Optional[float]]:
    """Sequential % growth, computed (never extracted)."""
    out: List[Optional[float]] = [None]
    for prev, cur in zip(values, values[1:]):
        out.append((cur - prev) / abs(prev) * 100 if prev not in (None, 0) and cur is not None else None)
    return out


def _bar_line(periods, bars, line, bar_label, line_label) -> str:
    fig, ax = plt.subplots(figsize=(3.5, 2.05))
    ax.bar(periods, [v or 0 for v in bars], color=TEAL, width=0.5, zorder=3)
    _clean(ax)
    ax.set_ylabel(bar_label, fontsize=7)
    ax.yaxis.set_major_locator(MaxNLocator(4))
    if line and any(v is not None for v in line):
        ax2 = ax.twinx()
        ax2.plot(periods, [v if v is not None else float("nan") for v in line],
                 color=ORANGE, marker="o", markersize=3, linewidth=1.4, zorder=4)
        ax2.set_ylabel(line_label, fontsize=7)
        ax2.spines["top"].set_visible(False)
        ax2.tick_params(length=0, colors=SLATE, labelsize=7)
        ax2.yaxis.set_major_locator(MaxNLocator(4))
    return _uri(fig)


def build_charts(report: ResearchReport) -> dict:
    """Returns {'grid': [[slot, slot], [slot, slot]]} of {'title','uri'} dicts."""
    slots = []
    q = report.quarterly
    fy = report.financials

    if len([x for x in q if x.sales_cr is not None]) >= 2:
        rows = [x for x in q if x.sales_cr is not None]
        p = [x.period for x in rows]
        sales = [x.sales_cr for x in rows]
        slots.append({"title": "Revenue", "uri": _bar_line(p, sales, _growth_series(sales), "Rs.cr", "Growth (QoQ)")})
        if any(x.ebitda_cr is not None for x in rows):
            slots.append({"title": "EBITDA", "uri": _bar_line(
                p, [x.ebitda_cr for x in rows], [x.ebitda_margin_pct for x in rows], "Rs.cr", "Margin (%)")})
        if any(x.adj_pat_cr is not None for x in rows):
            pat = [x.adj_pat_cr for x in rows]
            margin = [ (x.adj_pat_cr / x.sales_cr * 100) if (x.adj_pat_cr is not None and x.sales_cr) else None for x in rows]
            slots.append({"title": "PAT", "uri": _bar_line(p, pat, margin, "Rs.cr", "Margin (%)")})

    if len([f for f in fy if f.sales_cr is not None]) >= 2:
        rows = [f for f in fy if f.sales_cr is not None]
        p = [f.period for f in rows]
        slots.append({"title": "Annual Sales", "uri": _bar_line(
            p, [f.sales_cr for f in rows], [f.growth_pct for f in rows], "Rs.cr", "Growth (%)")})

    slots = slots[:4]
    grid = [slots[i:i + 2] for i in range(0, len(slots), 2)]
    for row in grid:
        while len(row) < 2:
            row.append(None)
    return {"grid": grid}
