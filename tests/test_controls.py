from pathlib import Path
import pandas as pd

def test_close_report_exists_after_controls_run():
    # Este teste assume que o CI rodou src/controls.py no passo "Smoke test"
    report_path = Path("reports") / "close_report.csv"
    assert report_path.exists(), "close_report.csv não foi gerado"

    df = pd.read_csv(report_path)
    assert "close_readiness_score" in df.columns
    assert df.loc[0, "close_readiness_score"] >= 0