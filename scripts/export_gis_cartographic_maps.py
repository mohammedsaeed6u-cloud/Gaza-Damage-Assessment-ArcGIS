#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIS Cartographic Map Export — A3 Landscape @ 300 DPI
=====================================================
Generates the three master map plates of the Gaza damage assessment
directly from the analysis GeoDatabase (UNOSAT points, classified
building footprints, Getis-Ord Gi* hot-spot grid):

  01_Timeline_Imagery_Comparison.(png|pdf)
  02_Building_Damage_Classification_Map.(png|pdf)
  03_Kernel_Density_Hotspots_Map.(png|pdf)

Data source : ArcGIS_Pro_Project/Gaza_GIS_Master_GDB.zip (FileGDB)
CRS         : WGS 1984 / UTM Zone 36N (EPSG:32636)
Fonts       : Amiri + Tajawal (OFL) — pass font dir via FONTS_DIR env.

Usage:
  python scripts/export_gis_cartographic_maps.py
"""

import os
import io
import sys
import zipfile
import tempfile

import numpy as np
import geopandas as gpd
import pyogrio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.font_manager import fontManager, FontProperties
from matplotlib.lines import Line2D
import rasterio
from rasterio.plot import show as rio_show

import arabic_reshaper
from bidi.algorithm import get_display

# ------------------------------------------------------------------ config
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDB_ZIP = os.path.join(ROOT, "ArcGIS_Pro_Project", "Gaza_GIS_Master_GDB.zip")
GDB_DIR = os.path.join(ROOT, "ArcGIS_Pro_Project", "Gaza_GIS_Master.gdb")
OUT = os.path.join(ROOT, "04_Cartographic_Exports")
RASTERS = os.path.join(ROOT, "ArcGIS_Pro_Project", "Gaza_City_Focus")
FONTS_DIR = os.environ.get("FONTS_DIR", "/tmp/fonts")

A3 = (16.54, 11.69)          # inches — A3 landscape
DPI = 300

COLORS = {
    "Destroyed":  (185 / 255, 28 / 255, 28 / 255),
    "Severe":     (234 / 255, 88 / 255, 12 / 255),
    "Moderate":   (245 / 255, 158 / 255, 11 / 255),
    "Possible":   (148 / 255, 163 / 255, 184 / 255),
    "Intact":     (203 / 255, 213 / 255, 225 / 255),
    "NotSig":     (226 / 255, 232 / 255, 240 / 255),
    "Hot90":      (253 / 255, 186 / 255, 116 / 255),
    "Hot95":      (249 / 255, 115 / 255, 22 / 255),
    "Hot99":      (185 / 255, 28 / 255, 28 / 255),
    "sea":        (224 / 255, 242 / 255, 254 / 255),
}

# ------------------------------------------------------------------ fonts
for _f in ("Amiri-Regular.ttf", "Amiri-Bold.ttf",
           "Tajawal-Regular.ttf", "Tajawal-Bold.ttf", "Tajawal-Medium.ttf"):
    _p = os.path.join(FONTS_DIR, _f)
    if os.path.exists(_p):
        fontManager.addfont(_p)

# NOTE: Amiri carries the full Arabic Presentation Forms block (U+FE70–FEFF)
# required by arabic_reshaper output; Tajawal does not — use Amiri for all Arabic.
AR_TITLE = FontProperties(fname=os.path.join(FONTS_DIR, "Amiri-Bold.ttf"))
AR_BODY = FontProperties(fname=os.path.join(FONTS_DIR, "Amiri-Regular.ttf"))
AR_BODY_B = FontProperties(fname=os.path.join(FONTS_DIR, "Amiri-Bold.ttf"))


def ar(text: str) -> str:
    """Shape Arabic text for matplotlib (visual order)."""
    return get_display(arabic_reshaper.reshape(text))


# ------------------------------------------------------------------ data
def open_gdb():
    """Return path to a readable FileGDB (extract zip on demand)."""
    if os.path.isdir(GDB_DIR):
        return GDB_DIR
    tmp = os.path.join(tempfile.gettempdir(), "gaza_gdb_runtime")
    if not os.path.isdir(tmp):
        os.makedirs(tmp, exist_ok=True)
        with zipfile.ZipFile(GDB_ZIP) as z:
            z.extractall(tmp)
    return os.path.join(tmp, "Gaza_GIS_Master.gdb")


def load(gdb, layer, **kw):
    return pyogrio.read_dataframe(gdb, layer=layer, **kw)


# ------------------------------------------------------------------ helpers
def add_north_arrow(ax, x, y, size=0.035):
    ax.annotate("", xy=(x, y + size), xytext=(x, y),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="#0f172a", lw=2))
    ax.text(x, y + size + 0.012, "N", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=13, fontweight="bold", color="#0f172a")


def clear_axis_labels(ax):
    ax.set_xlabel("")
    ax.set_ylabel("")


def add_scale_bar(ax, length_km, x=0.06, y=0.06):
    """Simple scale bar in axes fraction position, length in data units."""
    xlim = ax.get_xlim()
    span_m = xlim[1] - xlim[0]
    frac = (length_km * 1000.0) / span_m
    ax.plot([x, x + frac], [y, y], transform=ax.transAxes,
            color="#0f172a", lw=3.5, solid_capstyle="butt")
    for xi in (x, x + frac / 2, x + frac):
        ax.plot([xi, xi], [y - 0.008, y + 0.008], transform=ax.transAxes,
                color="#0f172a", lw=2)
    ax.text(x + frac / 2, y + 0.018, f"{int(length_km/2)}     {int(length_km)} km",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=9.5,
            color="#0f172a", family="DejaVu Sans")


def add_frame(ax):
    for s in ax.spines.values():
        s.set_edgecolor("#0f172a")
        s.set_linewidth(1.2)
    ax.set_xticks([]); ax.set_yticks([])


def title_block(fig, ar_title, en_title, subtitle_ar):
    fig.text(0.985, 0.978, ar(ar_title), ha="right", va="top",
             fontsize=27, fontproperties=AR_TITLE, color="#0f172a")
    fig.text(0.985, 0.923, en_title, ha="right", va="top",
             fontsize=12.5, color="#334155", family="DejaVu Sans")
    fig.text(0.985, 0.898, ar(subtitle_ar), ha="right", va="top",
             fontsize=12, fontproperties=AR_BODY, color="#475569")


def footer(fig, extra=""):
    base = ("الإسناد المكاني: WGS 1984 / UTM Zone 36N (EPSG:32636)   |   "
            "المصادر: UNOSAT CDA، OCHA، Copernicus Sentinel-2، OpenStreetMap/HOT   |   "
            "التحليل: GeoDatabase — FileGDB (ArcGIS Pro compatible)")
    fig.text(0.5, 0.030, ar(base + extra), ha="center", va="bottom",
             fontsize=9.5, fontproperties=AR_BODY, color="#64748b")
    fig.text(0.015, 0.012, "Gaza Spatial Damage Assessment — Master Plate",
             ha="left", va="bottom", fontsize=8.5, color="#94a3b8", family="DejaVu Sans")


def legend_box(ax, items, title_ar, x=0.015, y=0.985, fontsize=10.5):
    """items: list of (color, label_ar, label_en, count_str)"""
    handles = [
        Line2D([0], [0], marker="s", linestyle="", markersize=11,
               markerfacecolor=c, markeredgecolor="#334155", markeredgewidth=0.6)
        for (c, _, _, _) in items
    ]
    labels = [ar(f"{a}   {en}  {cnt}") for (_, a, en, cnt) in items]
    leg = ax.legend(handles, labels, loc="upper left",
                    bbox_to_anchor=(x, y), fontsize=fontsize,
                    prop=AR_BODY, frameon=True, title=ar(title_ar),
                    facecolor="white", edgecolor="#0f172a")
    leg.get_title().set_fontproperties(AR_BODY_B)
    leg.get_title().set_fontsize(fontsize + 1)
    return leg


# ------------------------------------------------------------------ MAP 02
def map_building_damage(gdb):
    print("→ loading Buildings_Classified_AR ...")
    bld = load(gdb, "Buildings_Classified_AR")
    gov = load(gdb, "Gaza_Governorates_AR")

    order = [
        (0, "Intact",    "سليم / غير متضرر", "Intact / Minor", COLORS["Intact"]),
        (4, "Possible",  "دمار محتمل",       "Possible Damage", COLORS["Possible"]),
        (3, "Moderate",  "دمار متوسط",       "Moderate Damage", COLORS["Moderate"]),
        (2, "Severe",    "دمار شديد",        "Severe Damage",   COLORS["Severe"]),
        (1, "Destroyed", "مدمر كلياً",        "Destroyed",       COLORS["Destroyed"]),
    ]

    fig, ax = plt.subplots(figsize=A3)
    ax.set_facecolor(COLORS["sea"])

    total = len(bld)
    for code, key, lab_ar, lab_en, col in order:
        sub = bld[bld["Damage_Code"] == code]
        if len(sub) == 0:
            continue
        sub.plot(ax=ax, color=col, edgecolor="none", rasterized=True)
        print(f"   plotted {key}: {len(sub):,}")

    gov.boundary.plot(ax=ax, color="#0f172a", linewidth=1.1)

    # governorate labels
    for _, r in gov.iterrows():
        p = r.geometry.representative_point()
        ax.annotate(ar(r["Gov_Name_A"]),
                    xy=(p.x, p.y), ha="center", va="center",
                    fontsize=13, fontproperties=AR_BODY_B,
                    bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#0f172a", lw=0.8, alpha=0.85))

    items = []
    for code, key, lab_ar, lab_en, col in order:
        n = int((bld["Damage_Code"] == code).sum())
        items.append((col, lab_ar, lab_en, f"({n:,} — {n/total*100:.1f}%)"))

    legend_box(ax, items, "تصنيف أضرار المباني — Buildings Damage Classes")
    add_north_arrow(ax, 0.93, 0.885)
    add_scale_bar(ax, 10)
    add_frame(ax)
    clear_axis_labels(ax)
    ax.set_xlim(gov.total_bounds[0] - 500, gov.total_bounds[2] + 500)
    ax.set_ylim(gov.total_bounds[1] - 500, gov.total_bounds[3] + 500)
    ax.set_aspect("equal")

    title_block(
        fig,
        "خريطة تصنيف أضرار المباني — قطاع غزة (2023–2026)",
        "Building Damage Classification Map — Gaza Strip   |   326,448 Footprints",
        "التصنيف مبني على تحليل بصري فائق الدقة UNOSAT CDA مع التحقق المتقاطع بالاستشعار عن بعد متعدد الحساسات",
    )
    footer(fig)
    fig.subplots_adjust(top=0.885, bottom=0.045, left=0.02, right=0.98)
    _save(fig, "02_Building_Damage_Classification_Map")
    plt.close(fig)


# ------------------------------------------------------------------ MAP 03
def map_hotspots(gdb):
    print("→ loading HotSpots grid + damage points ...")
    grid = load(gdb, "Gaza_HotSpots_Grid")
    pts = load(gdb, "UNOSAT_Damage_Points_AllStages")
    gov = load(gdb, "Gaza_Governorates_AR")

    cls_style = {
        "Not Significant":            (COLORS["NotSig"], "غير دال إحصائياً", "Not Significant"),
        "Hot Spot - 90% Confidence":  (COLORS["Hot90"],  "بؤرة ساخنة 90%",  "Hot Spot 90%"),
        "Hot Spot - 95% Confidence":  (COLORS["Hot95"],  "بؤرة ساخنة 95%",  "Hot Spot 95%"),
        "Hot Spot - 99% Confidence":  (COLORS["Hot99"],  "بؤرة ساخنة 99%",  "Hot Spot 99%"),
    }

    fig, ax = plt.subplots(figsize=A3)
    ax.set_facecolor(COLORS["sea"])

    for cls, (col, _, _) in cls_style.items():
        sub = grid[grid["HotSpot_Cl"] == cls]
        if len(sub) == 0:
            continue
        sub.plot(ax=ax, color=col, edgecolor="#64748b" if cls == "Not Significant" else "none",
                 linewidth=0.15 if cls == "Not Significant" else 0, rasterized=True)
        print(f"   plotted {cls}: {len(sub):,}")

    pts[pts["Damage_Cod"] == 1].plot(ax=ax, color="#475569", markersize=0.25,
                                     alpha=0.28, rasterized=True)
    gov.boundary.plot(ax=ax, color="#0f172a", linewidth=1.1)

    items = []
    for cls, (col, a, e) in cls_style.items():
        n = int((grid["HotSpot_Cl"] == cls).sum())
        items.append((col, a, e, f"({n:,})"))
    legend_box(ax, items, "تصنيف البؤر الساخنة — Getis-Ord Gi* (90/95/99%)")

    add_north_arrow(ax, 0.93, 0.885)
    add_scale_bar(ax, 10)
    add_frame(ax)
    clear_axis_labels(ax)
    ax.set_xlim(gov.total_bounds[0] - 500, gov.total_bounds[2] + 500)
    ax.set_ylim(gov.total_bounds[1] - 500, gov.total_bounds[3] + 500)
    ax.set_aspect("equal")

    title_block(
        fig,
        "خريطة البؤر الساخنة لدمار المباني — تحليل Getis-Ord Gi*",
        "Hot-Spot Analysis of Building Damage — Getis-Ord Gi* Z-Scores   |   6,146 Grid Cells",
        "النقاط الرمادية تمثل مواقع الدمار المؤكد (UNOSAT) — الشبكة المكانية 500م × 500م",
    )
    footer(fig)
    fig.subplots_adjust(top=0.885, bottom=0.045, left=0.02, right=0.98)
    _save(fig, "03_Kernel_Density_Hotspots_Map")
    plt.close(fig)


# ------------------------------------------------------------------ MAP 01
def map_timeline():
    print("→ loading timeline rasters ...")
    stages = [
        ("Gaza_City_1_Pre_Aug_2023.tif",     "خط الأساس — أغسطس 2023",   "Baseline — Aug 2023"),
        ("Gaza_City_2_Immediate_Nov_2023.tif", "المرحلة الأولى — نوفمبر 2023", "Phase 1 — Nov 2023"),
        ("Gaza_City_3_OneYear_Aug_2024.tif",  "المرحلة الثانية — أغسطس 2024", "Phase 2 — Aug 2024"),
        ("Gaza_City_4_Latest_Nov_2026.tif",   "الوضع الراهن — نوفمبر 2026",  "Present — Nov 2026"),
    ]
    fig = plt.figure(figsize=A3)
    fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(2, 2, left=0.035, right=0.965, top=0.858, bottom=0.075,
                          wspace=0.06, hspace=0.13)

    for i, (fn, ar_t, en_t) in enumerate(stages):
        ax = fig.add_subplot(gs[i // 2, i % 2])
        with rasterio.open(os.path.join(RASTERS, fn)) as src:
            arr = src.read()
            rio_show(arr, transform=src.transform, ax=ax)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#0f172a"); s.set_linewidth(1.1)
        ax.set_title(ar(ar_t) + "\n" + en_t, fontsize=14,
                     fontproperties=AR_BODY_B, color="#0f172a", pad=8)
        print(f"   panel {fn} ok")

    title_block(
        fig,
        "المقارنة الزمنية للمرئيات الفضائية — مدينة غزة (2023–2026)",
        "Multi-Temporal Sentinel-2 Imagery Comparison — Gaza City   |   10 m/px   |   UTM 36N",
        "أربع مراحل زمنية متجانسة اللون على شبكة مرجعية واحدة (629000–645500E / 3476500–3493000N)",
    )
    footer(fig)
    _save(fig, "01_Timeline_Imagery_Comparison")
    plt.close(fig)


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    png = os.path.join(OUT, name + ".png")
    pdf = os.path.join(OUT, name + ".pdf")
    fig.savefig(png, dpi=DPI, facecolor="white")
    print("   saved", png, f"({os.path.getsize(png)/1e6:.1f} MB)")
    fig.savefig(pdf, facecolor="white")
    print("   saved", pdf, f"({os.path.getsize(pdf)/1e6:.1f} MB)")


def main():
    gdb = open_gdb()
    print("GDB:", gdb)
    map_timeline()
    map_building_damage(gdb)
    map_hotspots(gdb)
    print("done.")


if __name__ == "__main__":
    main()
