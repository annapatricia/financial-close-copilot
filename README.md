
# Financial Close Copilot (ETL + RPA + ML)

![CI](https://github.com/annapatricia/financial-close-copilot/actions/workflows/ci.yml/badge.svg)

Projeto demonstrativo com dados fictícios para simular fechamento contábil mensal.

- RPA: ingestão/organização a partir de inbox/
- ETL: raw -> clean -> curated
- Controles: validações e checklist
- ML: detecção simples de anomalias / classificação
- Insights: KPIs e variação mês a mês

financial-close-copilot/
├─ app.py
├─ README.md
├─ requirements.txt
├─ runtime.txt
├─ .gitignore
├─ .streamlit/
│  └─ config.toml
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ src/
│  ├─ __init__.py
│  ├─ generate_fake_data.py
│  ├─ rpa_ingest.py
│  ├─ etl_transform.py
│  ├─ controls.py
│  ├─ ml_anomaly.py
│  └─ run_pipeline.py
├─ tests/
│  └─ test_controls.py
├─ data/
│  ├─ raw/        (NÃO versionar)
│  ├─ clean/      (NÃO versionar)
│  └─ curated/    (NÃO versionar)
├─ reports/       (NÃO versionar)
└─ inbox/         (pode manter .gitkeep) 
