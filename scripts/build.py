#!/usr/bin/env python3
"""Valida los JSON de data/<mercado>/*.json y genera data/index.json con los valores calculados.

Uso:  python3 scripts/build.py          # valida + genera
      python3 scripts/build.py --check  # solo valida (CI)

Fórmula (ver METODO.md):
    valor_usd_por_punto = (cash_usd - tasas_usd) / puntos
"""
import json
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STALE_DAYS = 90
REQUIRED_PROGRAM = {"id", "name", "unit", "market", "alternatives", "transfers"}
REQUIRED_MEASUREMENT = {"date", "cash", "points", "fees", "fx", "author"}

errors = []


def err(path, msg):
    errors.append(f"{path}: {msg}")


def to_usd(amount, currency, fx):
    if currency == "USD":
        return amount
    if currency == "ARS":
        return amount / fx["rate"]
    raise ValueError(f"moneda no soportada: {currency}")


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def load_program(path):
    try:
        p = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(path, f"JSON inválido: {e}")
        return None
    missing = REQUIRED_PROGRAM - set(p)
    if missing:
        err(path, f"faltan campos: {sorted(missing)}")
        return None
    if p["id"] != path.stem:
        err(path, f"id '{p['id']}' no coincide con el nombre del archivo")
    return p


def compute_measurement(path, m):
    missing = REQUIRED_MEASUREMENT - set(m)
    if missing:
        err(path, f"medición sin campos {sorted(missing)}")
        return None
    try:
        d = parse_date(m["date"])
    except ValueError:
        err(path, f"fecha inválida '{m['date']}' (usar AAAA-MM-DD)")
        return None
    if not m["cash"].get("source"):
        err(path, f"medición {m['date']} sin fuente de precio cash")
    if m["points"] <= 0:
        err(path, f"medición {m['date']} con puntos <= 0")
    fx = m["fx"]
    cash_usd = to_usd(m["cash"]["amount"], m["cash"]["currency"], fx)
    fees_usd = to_usd(m["fees"]["amount"], m["fees"]["currency"], fx)
    net = cash_usd - fees_usd
    if net <= 0:
        err(path, f"medición {m['date']}: tasas >= precio cash")
    usd_per_point = net / m["points"]
    age = (date.today() - d).days
    return {
        "date": m["date"],
        "window": m.get("window"),
        "cash_usd": round(cash_usd, 2),
        "fees_usd": round(fees_usd, 2),
        "net_usd": round(net, 2),
        "points": m["points"],
        "usd_per_point": usd_per_point,
        "cents_per_point": round(usd_per_point * 100, 3),
        "estimated": bool(m["fees"].get("estimated") or m["cash"].get("estimated")),
        "stale": age > STALE_DAYS,
        "age_days": age,
        "author": m["author"],
        "cash": m["cash"],
        "fees": m["fees"],
        "fx": fx,
        "notes": m.get("notes", ""),
    }


def build():
    programs = []
    for market_dir in sorted(p for p in DATA.iterdir() if p.is_dir()):
        for path in sorted(market_dir.glob("*.json")):
            p = load_program(path)
            if not p:
                continue
            out = {k: p[k] for k in ("id", "name", "unit", "market")}
            out["website"] = p.get("website")
            out["expiry"] = p.get("expiry")
            out["alternatives"] = []
            for alt in p["alternatives"]:
                ms = [compute_measurement(path, m) for m in alt.get("measurements", [])]
                ms = [m for m in ms if m]
                ms.sort(key=lambda m: m["date"], reverse=True)
                latest = ms[0] if ms else None
                out["alternatives"].append({
                    "id": alt["id"],
                    "label": alt["label"],
                    "type": alt.get("type"),
                    "reference": bool(alt.get("reference")),
                    "latest": latest,
                    "measurements": ms,
                    "confidence": len({m["author"] for m in ms if not m["stale"]}),
                })
            out["transfers"] = p["transfers"]
            # valor de referencia del programa = alternativa marcada reference, o la mejor vigente
            ref = next((a for a in out["alternatives"] if a["reference"] and a["latest"]), None)
            if not ref:
                cands = [a for a in out["alternatives"] if a["latest"]]
                ref = max(cands, key=lambda a: a["latest"]["usd_per_point"]) if cands else None
            out["reference_alternative"] = ref["id"] if ref else None
            out["reference_cents_per_point"] = ref["latest"]["cents_per_point"] if ref else None
            programs.append(out)
    return {"generated": date.today().isoformat(), "stale_days": STALE_DAYS, "programs": programs}


if __name__ == "__main__":
    index = build()
    if errors:
        print("ERRORES:\n  " + "\n  ".join(errors))
        sys.exit(1)
    if "--check" not in sys.argv:
        (DATA / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"OK: {len(index['programs'])} programas → data/index.json")
    else:
        print(f"OK: {len(index['programs'])} programas válidos")
    for p in index["programs"]:
        c = p["reference_cents_per_point"]
        print(f"  {p['name']:<42} {c if c is not None else '—':>8} ¢/{p['unit']}")
