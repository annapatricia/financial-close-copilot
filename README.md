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

---

---

## 🧩 Componentes do Projeto

### 🤖 1. RPA — Ingestão & Auditoria

| Item | Descrição |
|------|------------|
| **Script** | `src/rpa_ingest.py` |
| **Função** | Move arquivos de `inbox/` → `data/raw/` com timestamp |
| **Auditoria** | Gera `reports/audit_trail.csv` |

Automatiza o recebimento de arquivos e garante rastreabilidade.

---

### 🔄 2. ETL — RAW → CLEAN → CURATED

| Camada | Descrição |
|--------|------------|
| **RAW** | Arquivos ingeridos automaticamente |
| **CLEAN** | Padronização, remoção de duplicidade, conversão de tipos |
| **CURATED** | Geração de lançamentos contábeis simulados (D/C) |

Script principal:  
`src/etl_transform.py`

---

### 📊 3. Controles de Fechamento

Script: `src/controls.py`

Gera o relatório:

`reports/close_report.csv`

**Indicadores calculados:**

- Receita Total  
- Despesa Total  
- Lucro Estimado  
- Balance Issues (Diferença D vs C)  
- Close Readiness Score  

---

### 🧠 4. Machine Learning (Anomalias)

| Item | Descrição |
|------|------------|
| **Script** | `src/ml_anomaly.py` |
| **Modelo** | IsolationForest |
| **Saída** | `reports/anomalies_only.csv` |

Detecção simples de lançamentos atípicos.

---

## ⚙️ CI & Testes Automatizados

Workflow: `.github/workflows/ci.yml`

Executa automaticamente a cada `push`:

- Instala dependências  
- Roda smoke test do pipeline  
- Executa `pytest`

Rodar localmente:

```bash
pytest -q
