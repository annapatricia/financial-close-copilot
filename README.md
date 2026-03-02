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


Componentes do Projeto

O projeto está estruturado em cinco blocos principais que representam o fluxo completo do fechamento contábil: ingestão, transformação, controle, análise e visualização.

🤖 1. RPA — Ingestão & Auditoria

Script: src/rpa_ingest.py

Função:

Move arquivos recebidos de inbox/ para data/raw/

Aplica timestamp para versionamento

Gera trilha de auditoria

Output:

reports/audit_trail.csv

Objetivo:
Automatizar o recebimento de arquivos e garantir rastreabilidade completa do processo.

🔄 2. ETL — RAW → CLEAN → CURATED

Script principal: src/etl_transform.py

O pipeline segue arquitetura em camadas:

Camada	Descrição
RAW	Dados ingeridos automaticamente pelo RPA
CLEAN	Padronização de colunas, tratamento de tipos, remoção de duplicidades
CURATED	Base analítica final + geração de lançamentos contábeis simulados (Débito/Crédito)

Outputs principais:

data/clean/*

data/curated/fact_gl_entries.csv

Objetivo:
Transformar dados operacionais em base confiável para análise financeira.

📊 3. Controles de Fechamento

Script: src/controls.py

Output:

reports/close_report.csv

Indicadores calculados:

Receita Total

Despesa Total

Lucro Estimado

Diferença Débito vs Crédito

Close Readiness Score

Objetivo:
Validar consistência contábil e gerar indicador de prontidão do fechamento.

🧠 4. Machine Learning — Detecção de Anomalias (Opcional)

Script: src/ml_anomaly.py

Modelo utilizado: IsolationForest

Output:

reports/anomalies_only.csv

Objetivo:
Identificar lançamentos atípicos para priorização de revisão e mitigação de risco.

📈 5. Dashboard Executivo (Streamlit)

Arquivo: app.py

Funcionalidades:

Visualização de KPIs de fechamento

Resumo financeiro consolidado

Indicador de prontidão

Visualização de anomalias

Objetivo:
Traduzir o pipeline técnico em visão executiva orientada à decisão.
