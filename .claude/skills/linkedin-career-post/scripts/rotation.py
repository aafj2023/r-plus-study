#!/usr/bin/env python3
"""Memória estratégica + rotação de categorias para o LinkedIn Career Post v6.0.

--next    : escolhe a categoria (A-F) mais atrás da meta de distribuição e devolve
            os temas recentes a evitar (JSON no stdout).
--record  : registra o post publicado no histórico (mantém os últimos 100).

Sem dependências externas (stdlib apenas).
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join(HERE, "..", "memory", "history.json")

# Metas de distribuição do escopo v6.0
TARGETS = {"A": 0.15, "B": 0.25, "C": 0.20, "D": 0.20, "E": 0.10, "F": 0.10}
TYPE_NAMES = {
    "A": "Market Intelligence",
    "B": "FP&A Expertise",
    "C": "Strategic Finance",
    "D": "Business Partnering",
    "E": "Leadership Finance",
    "F": "Executive Thinking",
}
AVOID_WINDOW = 12   # nº de posts recentes cujos temas não devem repetir
MAX_HISTORY = 100


def load():
    if not os.path.exists(MEM):
        return []
    with open(MEM, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save(history):
    os.makedirs(os.path.dirname(MEM), exist_ok=True)
    with open(MEM, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def pick_next(history):
    """Categoria com maior déficit (meta - participação atual)."""
    total = len(history) or 1
    counts = {c: 0 for c in TARGETS}
    for p in history:
        c = p.get("category")
        if c in counts:
            counts[c] += 1
    # déficit = quanto a categoria está abaixo da meta
    deficits = {c: TARGETS[c] - counts[c] / total for c in TARGETS}
    # desempate estável: maior déficit, depois ordem alfabética
    best = sorted(deficits.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return best, counts


def cmd_next(_args):
    history = load()
    cat, counts = pick_next(history)
    avoid = [p.get("theme", "") for p in history[-AVOID_WINDOW:] if p.get("theme")]
    out = {
        "category": cat,
        "type_name": TYPE_NAMES[cat],
        "target_share": TARGETS[cat],
        "counts_so_far": counts,
        "total_posts": len(history),
        "avoid_themes": avoid,
        "sophistication_hint": (
            "iniciante" if len(history) < 10 else
            "intermediario" if len(history) < 40 else "avancado"
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_record(args):
    history = load()
    entry = {
        "n": len(history) + 1,
        "date": datetime.date.today().isoformat(),
        "category": args.category.upper(),
        "type_name": TYPE_NAMES.get(args.category.upper(), "?"),
        "theme": args.theme,
        "keywords": [k.strip() for k in args.keywords.split(",") if k.strip()],
        "seniority": args.seniority,
        "gap": args.gap,
    }
    history.append(entry)
    save(history)
    print(json.dumps({"recorded": entry, "history_size": len(history[-MAX_HISTORY:])},
                     ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--next", action="store_true")
    p.add_argument("--record", action="store_true")
    p.add_argument("--category", default="")
    p.add_argument("--theme", default="")
    p.add_argument("--keywords", default="")
    p.add_argument("--seniority", default="")
    p.add_argument("--gap", default="")
    args = p.parse_args()

    if args.next:
        cmd_next(args)
    elif args.record:
        if not args.category:
            sys.exit("--record requer --category (A-F)")
        cmd_record(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
