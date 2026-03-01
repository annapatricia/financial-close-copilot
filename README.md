![CI](https://github.com/annapatricia/financial-close-copilot/actions/workflows/ci.yml/badge.svg)

# Financial Close Copilot (ETL + RPA + ML)

Demo (Streamlit Cloud): https://SEU-APP.streamlit.app

Projeto demonstrativo com dados fictícios que simula um **fechamento contábil mensal**, com foco em:
- **RPA** (ingestão e auditoria de arquivos recebidos)
- **ETL** (camadas RAW → CLEAN → CURATED)
- **Controles de fechamento** (checks contábeis e indicador de prontidão)
- **ML** (detecção simples de anomalias)
- **Dashboard** (visão executiva com KPIs)

> Objetivo: demonstrar uma abordagem end-to-end para **integração multissetorial**, **automação** e **insights** no contexto de fechamento financeiro.

---

## Arquitetura (visão rápida)

1. **RPA Ingest** (`inbox/` → `data/raw/`) + `reports/audit_trail.csv`  
2. **ETL** (`data/raw/` → `data/clean/` → `data/curated/`)  
3. **Curated (GL)**: gera lançamentos contábeis simulados (`fact_gl_entries.csv`)  
4. **Controls**: validações e `reports/close_report.csv` (receita, despesa, lucro, score)  
5. **ML (opcional)**: anomalias (`reports/anomalies_only.csv`)  
6. **Dashboard**: KPIs e resumos para decisão

---

## Estrutura do repositório

```├─ app.py
├─ requirements.txt
├─ runtime.txt
├─ .streamlit/config.toml
├─ .github/workflows/ci.yml
├─ src/
│ ├─ generate_fake_data.py
│ ├─ rpa_ingest.py
│ ├─ etl_transform.py
│ ├─ controls.py
│ ├─ ml_anomaly.py
│ └─ run_pipeline.py
└─ tests/
└─ test_controls.py
```
```
├─ app.py
├─ requirements.txt
├─ runtime.txt
├─ .streamlit/config.toml
├─ .github/workflows/ci.yml
├─ src/
│ ├─ generate_fake_data.py
│ ├─ rpa_ingest.py
│ ├─ etl_transform.py
│ ├─ controls.py
│ ├─ ml_anomaly.py
│ └─ run_pipeline.py
└─ tests/
└─ test_controls.py
```


**Observação:** pastas de dados e outputs (`data/*`, `reports/*`) são geradas em runtime e não são versionadas (ver `.gitignore`).

---

## Como rodar localmente (Windows / PowerShell)

### 1) Instalar dependências
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest

2) Rodar o pipeline completo (RPA → ETL → Controls)
python src/run_pipeline.py

3) (Opcional) Rodar ML para anomalias
python src/ml_anomaly.py
4) Rodar o dashboard
streamlit run app.py

Componentes principais
RPA (ingestão + auditoria)

Script: src/rpa_ingest.py

Ação: move arquivos da inbox/ para data/raw/ com timestamp

Auditoria: reports/audit_trail.csv

ETL (RAW → CLEAN → CURATED)

Script: src/etl_transform.py

Clean: padronização, remoção de duplicidade, conversão de tipos

Curated: criação de lançamentos contábeis simulados (D/C)

Controles de fechamento

Script: src/controls.py

Gera reports/close_report.csv com:

Receita Total

Despesa Total

Lucro Estimado

Balance issues (diferença D vs C)

Close Readiness Score

ML (anomalias)

Script: src/ml_anomaly.py

Modelo: IsolationForest (baseline)

Output: reports/anomalies_only.csv

Testes e CI (GitHub Actions)

Workflow: .github/workflows/ci.yml

Executa:

instalação de dependências

smoke test do pipeline core

pytest

Rodar localmente:

pytest -q
Próximos passos (ideias de evolução)

Adicionar mais fontes (ex.: ERP/SAP simulado, rate FX, centros de custo)

Regras contábeis mais realistas (mapeamento de contas, conciliações)

Camadas de governança (versionamento de regras e trilha de auditoria)

Deploy “enterprise” com Docker + cloud (ECS/Fargate / Render)

Licença

Uso educacional / portfólio.


---

Se você me colar aqui o seu link final do app (`https://...streamlit.app`), eu devolvo a linha já preenchida certinha (e, se quiser, com um badge “Open in Streamlit”).

