import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# Criar pasta raw se não existir
Path("data/raw").mkdir(parents=True, exist_ok=True)

# --- AP (Contas a pagar)
ap = pd.DataFrame({
    "invoice_id": range(1001, 1011),
    "vendor": np.random.choice(["Fornecedor A", "Fornecedor B", "Fornecedor C"], 10),
    "amount": np.random.normal(5000, 1500, 10).round(2),
    "invoice_date": pd.date_range("2024-12-01", periods=10, freq="D"),
    "cost_center": np.random.choice(["TI", "Financeiro", "RH"], 10)
})

ap.to_csv("data/raw/ap_invoices.csv", index=False)

# --- AR (Contas a receber)
ar = pd.DataFrame({
    "invoice_id": range(2001, 2011),
    "customer": np.random.choice(["Cliente X", "Cliente Y", "Cliente Z"], 10),
    "amount": np.random.normal(8000, 2000, 10).round(2),
    "invoice_date": pd.date_range("2024-12-01", periods=10, freq="D"),
    "region": np.random.choice(["Sul", "Sudeste", "Nordeste"], 10)
})

ar.to_csv("data/raw/ar_invoices.csv", index=False)

print("Dados fictícios gerados com sucesso em data/raw/")