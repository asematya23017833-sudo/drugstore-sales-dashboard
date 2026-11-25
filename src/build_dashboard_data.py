"""Pharmaceutical (drugstore) Sales Dashboard - rebuild (Nov 2026).

Dataset: Rossmann Store Sales (public Kaggle competition dataset, mirrored on
GitHub) - 1,017,209 daily sales rows for 1,115 drugstores, 2013-2015. This is
a substitute dataset: the original sales file was lost. Rossmann is a
pharmacy/drugstore retail chain, matching the project's pharma-sales theme.
Computes the KPI set and exports chart-ready aggregates + PNG charts.
"""
import json
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
con = duckdb.connect()

kpis = con.execute(f"""
WITH sales AS (
  SELECT t.*, s.StoreType, s.Assortment
  FROM read_csv_auto('{ROOT}/data/rossmann_train.csv') t
  JOIN read_csv_auto('{ROOT}/data/rossmann_store.csv') s USING (Store)
  WHERE t.Open = 1
)
SELECT
  COUNT(*) AS transactions,
  COUNT(DISTINCT Store) AS stores,
  ROUND(SUM(Sales), 2) AS total_sales_eur,
  ROUND(AVG(Sales), 2) AS avg_daily_sales_eur,
  ROUND(SUM(Customers) * 1.0 / COUNT(*), 1) AS avg_daily_customers,
  MIN(Date) AS first_date, MAX(Date) AS last_date
FROM sales
""").df()

by_month = con.execute(f"""
SELECT DATE_TRUNC('month', CAST(Date AS DATE)) AS month, ROUND(SUM(Sales)/1e6, 2) AS sales_meur
FROM read_csv_auto('{ROOT}/data/rossmann_train.csv') WHERE Open = 1
GROUP BY 1 ORDER BY 1
""").df()

by_type = con.execute(f"""
SELECT s.StoreType, ROUND(SUM(t.Sales)/1e6, 2) AS sales_meur, ROUND(AVG(t.Sales), 0) AS avg_daily_sales
FROM read_csv_auto('{ROOT}/data/rossmann_train.csv') t
JOIN read_csv_auto('{ROOT}/data/rossmann_store.csv') s USING (Store)
WHERE t.Open = 1 GROUP BY 1 ORDER BY 2 DESC
""").df()

promo = con.execute(f"""
SELECT CASE WHEN Promo = 1 THEN 'Promo' ELSE 'No promo' END AS promo,
       ROUND(AVG(Sales), 0) AS avg_daily_sales, ROUND(AVG(Customers), 0) AS avg_customers
FROM read_csv_auto('{ROOT}/data/rossmann_train.csv') WHERE Open = 1 GROUP BY 1
""").df()

top_stores = con.execute(f"""
SELECT Store, ROUND(SUM(Sales)/1e6, 2) AS sales_meur
FROM read_csv_auto('{ROOT}/data/rossmann_train.csv') WHERE Open = 1
GROUP BY 1 ORDER BY 2 DESC LIMIT 10
""").df()

# charts
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pd.to_datetime(by_month["month"]), by_month["sales_meur"], marker="o", lw=1.5)
ax.set_title("Monthly sales (EUR millions), 2013-2015"); ax.set_ylabel("EUR m")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "monthly_sales.png", dpi=120); plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].bar(by_type["StoreType"], by_type["sales_meur"]); axes[0].set_title("Sales by store type"); axes[0].set_ylabel("EUR m")
axes[1].bar(promo["promo"], promo["avg_daily_sales"]); axes[1].set_title("Avg daily sales: promo effect"); axes[1].set_ylabel("EUR")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "storetype_promo.png", dpi=120); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(top_stores["Store"].astype(str), top_stores["sales_meur"])
ax.set_title("Top 10 stores by total sales"); ax.set_xlabel("Store"); ax.set_ylabel("EUR m")
fig.tight_layout(); fig.savefig(ROOT / "charts" / "top_stores.png", dpi=120); plt.close(fig)

summary = {"kpis": kpis.to_dict("records")[0],
           "sales_by_store_type": by_type.to_dict("records"),
           "promo_effect": promo.to_dict("records")}
(ROOT / "results.json").write_text(json.dumps(summary, indent=2, default=str))
print(json.dumps(summary, indent=2, default=str))
