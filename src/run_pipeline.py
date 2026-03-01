import subprocess
import sys

def run(cmd: list[str]) -> None:
    print("\n== Running:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)

def main() -> None:
    # 1) RPA - ingestão
    run([sys.executable, "src/rpa_ingest.py"])

    # 2) ETL - raw -> clean -> curated
    run([sys.executable, "src/etl_transform.py"])

    # 3) Controles - relatório do fechamento
    run([sys.executable, "src/controls.py"])

    print("\nPipeline completo ✅ (RPA -> ETL -> Controles)")

if __name__ == "__main__":
    main()