"""Drugstore Sales Dashboard - Streamlit companion app (rebuild, Nov 2026).
Interactive version of the verified analysis in src/build_dashboard_data.py.
Dataset: Rossmann Store Sales (public substitute dataset).
The dataset does not state a currency, so all values are reported as "sales units".
"""
import pathlib
import subprocess
import sys

if not (pathlib.Path(__file__).parent / "data" / "rossmann_train.csv").exists():
    subprocess.run([sys.executable, str(pathlib.Path(__file__).parent / "data" / "get_data.py")], check=True)

import altair as alt
import duckdb
import streamlit as st

st.set_page_config(page_title="Drugstore Sales Dashboard", layout="wide")
st.title("Drugstore (Pharmacy Retail) Sales Dashboard")
st.caption(
    "Rossmann Store Sales, public dataset - 1,017,209 daily rows, 1,115 stores, 2013-2015. "
    "Rebuild Nov 2026. The dataset states no currency; values are sales units."
)


@st.cache_data
def load():
    con = duckdb.connect()
    base = """FROM read_csv_auto('data/rossmann_train.csv') t
              JOIN read_csv_auto('data/rossmann_store.csv') s USING (Store) WHERE t.Open = 1"""
    kpi = con.execute(f"SELECT COUNT(*) n, SUM(t.Sales) sales, AVG(t.Sales) avg_s, COUNT(DISTINCT Store) st {base}").df()
    monthly = con.execute(f"SELECT DATE_TRUNC('month', CAST(t.Date AS DATE)) m, SUM(t.Sales)/1e6 v {base} GROUP BY 1 ORDER BY 1").df()
    bytype = con.execute(f"SELECT s.StoreType, SUM(t.Sales)/1e6 v {base} GROUP BY 1 ORDER BY 2 DESC").df()
    promo = con.execute(f"SELECT CASE WHEN t.Promo=1 THEN 'Promo days' ELSE 'No-promo days' END p, AVG(t.Sales) v {base} GROUP BY 1").df()
    top = con.execute(f"SELECT CAST(t.Store AS VARCHAR) store, SUM(t.Sales)/1e6 v {base} GROUP BY 1 ORDER BY 2 DESC LIMIT 10").df()
    return kpi, monthly, bytype, promo, top


kpi, monthly, bytype, promo, top = load()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Trading days", f"{int(kpi['n'][0]):,}")
c2.metric("Stores", f"{int(kpi['st'][0]):,}")
c3.metric("Total sales", f"{kpi['sales'][0] / 1e9:.2f}B units")
c4.metric("Avg daily sales per store", f"{kpi['avg_s'][0]:,.0f} units")

st.subheader("Monthly sales (millions of sales units)")
st.line_chart(monthly.set_index("m"))

left, right = st.columns(2)
left.subheader("Sales by store type (millions of sales units)")
left.altair_chart(
    alt.Chart(bytype)
    .mark_bar()
    .encode(
        x=alt.X("StoreType:N", title="Store type", sort="-y"),
        y=alt.Y("v:Q", title="Sales units (millions)"),
    ),
    use_container_width=True,
)
right.subheader("Promo vs no-promo days (avg daily sales units)")
right.caption("Observed association in the data, not a causal effect estimate.")
right.altair_chart(
    alt.Chart(promo)
    .mark_bar()
    .encode(
        x=alt.X("p:N", title=None, sort="-y"),
        y=alt.Y("v:Q", title="Avg daily sales units"),
    ),
    use_container_width=True,
)

st.subheader("Top 10 stores by total sales (millions of sales units, sorted)")
st.altair_chart(
    alt.Chart(top)
    .mark_bar()
    .encode(
        x=alt.X("store:N", title="Store", sort=None),
        y=alt.Y("v:Q", title="Sales units (millions)"),
    ),
    use_container_width=True,
)
