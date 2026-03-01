from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import csv

INBOX_DIR = Path("inbox")
RAW_DIR = Path("data/raw")
REPORTS_DIR = Path("reports")
AUDIT_FILE = REPORTS_DIR / "audit_trail.csv"

ALLOWED_EXTS = {".csv"}

def ensure_dirs() -> None:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_allowed_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in ALLOWED_EXTS

def safe_destination_name(src: Path) -> Path:
    """
    Evita sobrescrever arquivo existente em data/raw.
    Se já existir, cria sufixo _v2, _v3, ...
    """
    base = src.stem
    ext = src.suffix.lower()

    # padroniza o nome: <stem>__ingested_YYYYMMDD_HHMMSS.csv
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate = RAW_DIR / f"{base}__ingested_{ts}{ext}"

    if not candidate.exists():
        return candidate

    # fallback ultra-raro: se por acaso existir, acrescenta versão
    i = 2
    while True:
        alt = RAW_DIR / f"{base}__ingested_{ts}_v{i}{ext}"
        if not alt.exists():
            return alt
        i += 1

def append_audit_row(row: dict) -> None:
    file_exists = AUDIT_FILE.exists()
    with AUDIT_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "action", "source_path", "dest_path", "status", "notes"],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def ingest_one(file_path: Path) -> None:
    if not is_allowed_file(file_path):
        append_audit_row({
            "timestamp": now_iso(),
            "action": "INGEST",
            "source_path": str(file_path),
            "dest_path": "",
            "status": "SKIPPED",
            "notes": "Extensão não permitida",
        })
        return

    dest = safe_destination_name(file_path)

    try:
        shutil.move(str(file_path), str(dest))
        append_audit_row({
            "timestamp": now_iso(),
            "action": "INGEST",
            "source_path": str(file_path),
            "dest_path": str(dest),
            "status": "OK",
            "notes": "",
        })
        print(f"OK  - movido: {file_path.name} -> {dest.name}")
    except Exception as e:
        append_audit_row({
            "timestamp": now_iso(),
            "action": "INGEST",
            "source_path": str(file_path),
            "dest_path": str(dest),
            "status": "ERROR",
            "notes": repr(e),
        })
        print(f"ERRO - {file_path.name}: {e}")

def main() -> None:
    ensure_dirs()

    files = sorted([p for p in INBOX_DIR.iterdir() if p.is_file()])
    if not files:
        print("Inbox vazia. Nada para ingerir.")
        return

    print(f"Arquivos encontrados na inbox: {len(files)}")
    for p in files:
        ingest_one(p)

    print(f"Auditoria atualizada em: {AUDIT_FILE}")

if __name__ == "__main__":
    main()