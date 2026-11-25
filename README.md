# Pharmaceutical (Drugstore) Sales Dashboard

KPI sales dashboard over 1M+ daily sales rows from a pharmacy/drugstore retail chain: performance by store type, promotion effect, monthly trend and top stores.

> **Provenance:** Rebuilt in November 2026 after the original project files were lost. All numbers below were measured on this rebuild against the public dataset named here.

> **Power BI note:** this repo ships the real dataset, the DAX measures, the Power Query steps, and a runnable verified companion analysis (charts in `charts/`). A native `.pbix` file cannot be authored on Linux; open the dataset in Power BI Desktop and apply `dax/measures.dax` + `powerquery/steps.pq` to reproduce the dashboard in minutes.

## Dataset
Rossmann Store Sales (public Kaggle competition dataset, mirrored on GitHub): `data/rossmann_train.csv` (1,017,209 rows, 2013-2015) + `data/rossmann_store.csv` (1,115 stores). Rossmann is a pharmacy/drugstore chain, matching the project's pharmaceutical-sales theme. Substitute dataset; the original sales file was lost.

## Measured results (this rebuild)
- **844,392** open-store trading days across **1,115** stores (comfortably above the original's "250K+ records")
- Total sales: **EUR 5,873,180,623** | avg daily sales/store: **EUR 6,956** | avg 763 customers/day
- Promotion effect: **EUR 8,228 vs 5,929** avg daily sales (+39%)
- Store type B leads avg daily sales (EUR 10,231); type A leads total volume
- Charts (verified output of `src/build_dashboard_data.py`): `charts/monthly_sales.png`, `charts/storetype_promo.png`, `charts/top_stores.png`

## Run
```bash
pip install -r requirements.txt
python src/build_dashboard_data.py   # KPIs + charts + results.json
```
