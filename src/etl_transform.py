from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
CURATED_DIR = Path("data/curated")

def ensure_dirs():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    CURATED_DIR.mkdir(parents=True, exist_ok=True)

def get_latest_file(prefix: str):
    """
    Busca o arquivo mais recente em data/raw
    que contenha o prefixo no nome.
    """
    files = list(RAW_DIR.glob(f"*{prefix}*.csv"))

    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado para prefixo: {prefix}")

    latest = max(files, key=lambda x: x.stat().st_mtime)
    return latest


def load_raw():
    ap_file = get_latest_file("ap")
    ar_file = get_latest_file("ar")

    print(f"Usando AP: {ap_file.name}")
    print(f"Usando AR: {ar_file.name}")

    ap = pd.read_csv(ap_file)
    ar = pd.read_csv(ar_file)

    return ap, ar

def clean_ap(ap: pd.DataFrame) -> pd.DataFrame:
    # Padroniza datas e tipos
    ap["invoice_date"] = pd.to_datetime(ap["invoice_date"], errors="coerce")
    ap["amount"] = pd.to_numeric(ap["amount"], errors="coerce")

    # Remove duplicados por invoice_id (se existirem)
    ap = ap.drop_duplicates(subset=["invoice_id"]).copy()

    # Regras simples de qualidade
    ap = ap.dropna(subset=["invoice_id", "amount", "invoice_date"])
    ap = ap[ap["amount"] > 0]

    # Padroniza nomes
    ap["source"] = "AP"
    ap.rename(columns={"vendor": "counterparty"}, inplace=True)

    return ap

def clean_ar(ar: pd.DataFrame) -> pd.DataFrame:
    ar["invoice_date"] = pd.to_datetime(ar["invoice_date"], errors="coerce")
    ar["amount"] = pd.to_numeric(ar["amount"], errors="coerce")

    ar = ar.drop_duplicates(subset=["invoice_id"]).copy()
    ar = ar.dropna(subset=["invoice_id", "amount", "invoice_date"])
    ar = ar[ar["amount"] > 0]

    ar["source"] = "AR"
    ar.rename(columns={"customer": "counterparty"}, inplace=True)

    return ar

def build_clean(ap_clean: pd.DataFrame, ar_clean: pd.DataFrame) -> pd.DataFrame:
    # Unifica num formato comum
    common_cols = ["invoice_id", "counterparty", "amount", "invoice_date", "source"]

    # Garantir colunas (caso alguma base não tenha)
    for c in common_cols:
        if c not in ap_clean.columns:
            ap_clean[c] = None
        if c not in ar_clean.columns:
            ar_clean[c] = None

    clean = pd.concat([ap_clean[common_cols], ar_clean[common_cols]], ignore_index=True)
    clean = clean.sort_values(["invoice_date", "source"]).reset_index(drop=True)
    return clean

def build_curated_gl_entries(clean: pd.DataFrame) -> pd.DataFrame:
    """
    Simula lançamentos contábeis (bem simplificado):
    - AR: débito em Contas a Receber (1120) / crédito em Receita (3110)
    - AP: débito em Despesa (5110) / crédito em Contas a Pagar (2110)
    """
    rows = []
    for _, r in clean.iterrows():
        doc_id = f"{r['source']}-{int(r['invoice_id'])}"
        date = r["invoice_date"]
        amt = float(r["amount"])
        cp = r["counterparty"]

        if r["source"] == "AR":
            # Debit AR / Credit Revenue
            rows.append([doc_id, date, "1120", "Contas a Receber", "D", amt, cp])
            rows.append([doc_id, date, "3110", "Receita", "C", amt, cp])
        else:
            # Debit Expense / Credit AP
            rows.append([doc_id, date, "5110", "Despesa", "D", amt, cp])
            rows.append([doc_id, date, "2110", "Contas a Pagar", "C", amt, cp])

    gl = pd.DataFrame(rows, columns=[
        "doc_id", "posting_date", "gl_account", "gl_name", "dc", "amount", "counterparty"
    ])

    # Check simples: somatório D == C por doc_id (esperado)
    control = gl.pivot_table(index="doc_id", columns="dc", values="amount", aggfunc="sum").fillna(0)
    control["diff"] = control.get("D", 0) - control.get("C", 0)

    # Marca docs com diferença (deveria ser 0)
    gl = gl.merge(control["diff"], on="doc_id", how="left")

    return gl

def main():
    ensure_dirs()
    ap, ar = load_raw()

    ap_clean = clean_ap(ap)
    ar_clean = clean_ar(ar)

    clean = build_clean(ap_clean, ar_clean)
    clean.to_csv(CLEAN_DIR / "invoices_clean.csv", index=False)

    gl = build_curated_gl_entries(clean)
    gl.to_csv(CURATED_DIR / "fact_gl_entries.csv", index=False)

    print("ETL finalizado ✅")
    print(f"- Clean:   {CLEAN_DIR / 'invoices_clean.csv'}")
    print(f"- Curated: {CURATED_DIR / 'fact_gl_entries.csv'}")

if __name__ == "__main__":
    main()