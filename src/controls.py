from pathlib import Path
import pandas as pd

CURATED_DIR = Path("data/curated")
REPORTS_DIR = Path("reports")

def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_gl():
    return pd.read_csv(CURATED_DIR / "fact_gl_entries.csv")

def check_balance(gl: pd.DataFrame):
    summary = gl.pivot_table(
        index="doc_id",
        columns="dc",
        values="amount",
        aggfunc="sum"
    ).fillna(0)

    summary["diff"] = summary.get("D", 0) - summary.get("C", 0)
    issues = summary[summary["diff"] != 0].reset_index()

    return issues

def calculate_kpis(gl: pd.DataFrame):
    summary = gl.groupby("gl_name")["amount"].sum().reset_index()

    receita = summary.loc[summary["gl_name"] == "Receita", "amount"].sum()
    despesa = summary.loc[summary["gl_name"] == "Despesa", "amount"].sum()

    lucro = receita - despesa

    return receita, despesa, lucro

def close_score(issues_count: int):
    if issues_count == 0:
        return 100
    elif issues_count < 3:
        return 80
    else:
        return 50

def main():
    ensure_dirs()
    gl = load_gl()

    issues = check_balance(gl)
    receita, despesa, lucro = calculate_kpis(gl)
    score = close_score(len(issues))

    report = pd.DataFrame({
        "receita_total": [receita],
        "despesa_total": [despesa],
        "lucro_estimado": [lucro],
        "balance_issues": [len(issues)],
        "close_readiness_score": [score]
    })

    report.to_csv(REPORTS_DIR / "close_report.csv", index=False)

    print("Relatório de fechamento gerado ✅")
    print(report)

if __name__ == "__main__":
    main()