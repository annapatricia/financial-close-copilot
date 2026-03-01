from pathlib import Path
import pandas as pd

CURATED_DIR = Path("data/curated")
REPORTS_DIR = Path("reports")

def main():
    gl = pd.read_csv(CURATED_DIR / "fact_gl_entries.csv")
    gl["posting_date"] = pd.to_datetime(gl["posting_date"])

    gl["year_month"] = gl["posting_date"].dt.to_period("M")

    summary = (
        gl.groupby(["year_month", "gl_name"])["amount"]
        .sum()
        .reset_index()
    )

    summary = summary.sort_values("year_month")

    summary["variation_vs_previous"] = summary.groupby("gl_name")["amount"].pct_change()

    summary.to_csv(REPORTS_DIR / "kpi_monthly_variation.csv", index=False)

    print("KPI mensal gerado ✅")
    print(summary)

if __name__ == "__main__":
    main()