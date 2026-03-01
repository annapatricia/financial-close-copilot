from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest

CURATED_DIR = Path("data/curated")
REPORTS_DIR = Path("reports")

def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_gl():
    return pd.read_csv(CURATED_DIR / "fact_gl_entries.csv")

def detect_anomalies(gl: pd.DataFrame):
    # Usaremos apenas valor como exemplo simples
    model = IsolationForest(contamination=0.1, random_state=42)

    gl_numeric = gl[["amount"]].copy()

    model.fit(gl_numeric)
    gl["anomaly_flag"] = model.predict(gl_numeric)

    # -1 = anomalia, 1 = normal
    anomalies = gl[gl["anomaly_flag"] == -1]

    return gl, anomalies

def main():
    ensure_dirs()
    gl = load_gl()

    gl_scored, anomalies = detect_anomalies(gl)

    gl_scored.to_csv(REPORTS_DIR / "gl_with_anomalies.csv", index=False)
    anomalies.to_csv(REPORTS_DIR / "anomalies_only.csv", index=False)

    print("Detecção de anomalias concluída ✅")
    print(f"Total de lançamentos: {len(gl)}")
    print(f"Anomalias detectadas: {len(anomalies)}")

if __name__ == "__main__":
    main()