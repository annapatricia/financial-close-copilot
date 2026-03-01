from pathlib import Path
import pandas as pd
import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="Financial Close Copilot", layout="wide")

REPORTS_DIR = Path("reports")
CURATED_DIR = Path("data/curated")

st.title("📊 Financial Close Copilot")
st.caption("Dashboard simples para simular o fechamento contábil mensal (ETL + Controles + ML + RPA).")

# --------- Helpers ----------
def load_close_report():
    fp = REPORTS_DIR / "close_report.csv"
    if fp.exists():
        return pd.read_csv(fp)
    return None

def load_gl():
    fp = CURATED_DIR / "fact_gl_entries.csv"
    if fp.exists():
        df = pd.read_csv(fp)
        df["posting_date"] = pd.to_datetime(df["posting_date"], errors="coerce")
        return df
    return None

def load_anomalies():
    fp = REPORTS_DIR / "anomalies_only.csv"
    if fp.exists():
        return pd.read_csv(fp)
    return None

# --------- Sidebar ----------
st.sidebar.header("⚙️ Controles")
refresh = st.sidebar.button("Recarregar dados")

def ensure_artifacts():
    close_fp = REPORTS_DIR / "close_report.csv"
    gl_fp = CURATED_DIR / "fact_gl_entries.csv"

    if close_fp.exists() and gl_fp.exists():
        return

    st.warning("Arquivos do pipeline não encontrados. Rodando pipeline automaticamente (RPA → ETL → Controles)...")
    try:
        subprocess.run([sys.executable, "src/run_pipeline.py"], check=True)
        st.success("Pipeline executado com sucesso ✅")
    except Exception as e:
        st.error(f"Falha ao executar pipeline: {e}")
        st.stop()

ensure_artifacts()

close_report = load_close_report()
gl = load_gl()
anoms = load_anomalies()

if close_report is None or gl is None:
    st.warning("Não encontrei os arquivos do pipeline. Rode primeiro: `python src/run_pipeline.py` (e o ML se quiser anomalias).")
    st.stop()

# --------- KPIs ----------
row = close_report.iloc[0].to_dict()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Receita Total", f"{row.get('receita_total', 0):,.2f}")
c2.metric("Despesa Total", f"{row.get('despesa_total', 0):,.2f}")
c3.metric("Lucro Estimado", f"{row.get('lucro_estimado', 0):,.2f}")
c4.metric("Close Readiness Score", f"{int(row.get('close_readiness_score', 0))}")

st.markdown("---")

# --------- Resumo por conta ----------
st.subheader("Resumo por conta (GL)")

summary = (
    gl.groupby(["gl_name", "dc"], as_index=False)["amount"]
    .sum()
    .sort_values(["gl_name", "dc"])
)

left, right = st.columns([1, 1])

with left:
    st.dataframe(summary, use_container_width=True)

with right:
    pivot = gl.pivot_table(index="gl_name", columns="dc", values="amount", aggfunc="sum").fillna(0)
    # gráfico simples: receita e despesa (onde existir)
    chart_df = pivot.copy()
    if "D" not in chart_df.columns:
        chart_df["D"] = 0.0
    if "C" not in chart_df.columns:
        chart_df["C"] = 0.0
    st.bar_chart(chart_df[["D", "C"]])

st.markdown("---")

# --------- Séries por data ----------
st.subheader("Evolução (por data)")

daily = (
    gl.dropna(subset=["posting_date"])
      .groupby(["posting_date", "gl_name"], as_index=False)["amount"]
      .sum()
      .sort_values("posting_date")
)

st.line_chart(daily.pivot(index="posting_date", columns="gl_name", values="amount").fillna(0))

st.markdown("---")

# --------- Anomalias (se existir) ----------
st.subheader("Anomalias (ML)")

if anoms is None or len(anoms) == 0:
    st.info("Nenhuma anomalia encontrada (ou o arquivo não existe). Para gerar: rode `python src/ml_anomaly.py`.")
else:
    st.write(f"Total de anomalias: **{len(anoms)}**")
    st.dataframe(anoms.sort_values("amount", ascending=False), use_container_width=True)