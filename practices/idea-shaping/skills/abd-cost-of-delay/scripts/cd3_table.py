"""
Generate revenue vs opportunity-cost tables for CD3 ordering comparisons.

Usage:
  python cd3_table.py --items "A:1:5, B:4:1, C:5:2"
  python cd3_table.py --items "A:1:5, B:4:1, C:5:2" --order "B,C,A"
  python cd3_table.py --items "A:1:5, B:4:1, C:5:2" --compare "A,B,C" "B,C,A"
  python cd3_table.py --json items.json

Item format: Name:CoD:Duration (CoD per period, Duration in periods)
Period unit is flexible (weeks or months) — label it in your canvas.

Outputs a markdown table showing per-period: which item is being worked on,
which items are earning, revenue gained, and opportunity cost.
"""

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class Item:
    name: str
    cod: float  # cost of delay per period
    duration: int  # periods to deliver


def parse_items(items_str: str) -> list[Item]:
    items = []
    for part in items_str.split(","):
        part = part.strip()
        tokens = part.split(":")
        if len(tokens) != 3:
            print(f"ERROR: '{part}' must be Name:CoD:Duration", file=sys.stderr)
            sys.exit(1)
        items.append(Item(name=tokens[0].strip(), cod=float(tokens[1]), duration=int(tokens[2])))
    return items


def cd3_order(items: list[Item]) -> list[Item]:
    return sorted(items, key=lambda i: i.cod / i.duration, reverse=True)


def resolve_order(items: list[Item], order_str: str) -> list[Item]:
    name_map = {i.name: i for i in items}
    ordered = []
    for name in order_str.split(","):
        name = name.strip()
        if name not in name_map:
            print(f"ERROR: '{name}' not in items ({[i.name for i in items]})", file=sys.stderr)
            sys.exit(1)
        ordered.append(name_map[name])
    return ordered


def build_table(items: list[Item], order: list[Item]) -> dict:
    total_periods = sum(i.duration for i in order)
    max_cod = sum(i.cod for i in items)

    rows = []
    delivered = set()
    period = 0
    for current_item in order:
        for _ in range(current_item.duration):
            period += 1
            earning = {i.name: i.cod for i in items if i.name in delivered}
            revenue = sum(earning.values())
            opp_cost = max_cod - revenue
            rows.append({
                "period": period,
                "working_on": current_item.name,
                "earning": earning,
                "revenue": revenue,
                "opportunity_cost": opp_cost,
            })
        delivered.add(current_item.name)

    total_revenue = sum(r["revenue"] for r in rows)
    total_opp_cost = sum(r["opportunity_cost"] for r in rows)

    return {
        "order": [i.name for i in order],
        "rows": rows,
        "total_revenue": total_revenue,
        "total_opportunity_cost": total_opp_cost,
        "total_periods": total_periods,
    }


def format_table(items: list[Item], result: dict, period_label: str = "Period") -> str:
    item_names = [i.name for i in items]
    order_label = " > ".join(result["order"])

    header_cols = [period_label, "Working on"] + [f"{n} earning" for n in item_names] + ["Revenue", "Opp cost"]
    sep_cols = ["---", "---"] + ["---:"] * (len(item_names) + 2)

    lines = [f"**Order: {order_label}**", ""]
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("| " + " | ".join(sep_cols) + " |")

    for row in result["rows"]:
        earning_cells = []
        for name in item_names:
            val = row["earning"].get(name, 0)
            earning_cells.append(f"${val:,.0f}" if val > 0 else "-")
        cols = [
            str(row["period"]),
            row["working_on"],
        ] + earning_cells + [
            f"${row['revenue']:,.0f}",
            f"${row['opportunity_cost']:,.0f}",
        ]
        lines.append("| " + " | ".join(cols) + " |")

    lines.append(
        f"| **Total** | | "
        + " | ".join([""] * len(item_names))
        + f" | **${result['total_revenue']:,.0f}** | **${result['total_opportunity_cost']:,.0f}** |"
    )
    lines.append("")
    return "\n".join(lines)


def format_summary(items: list[Item]) -> str:
    lines = ["**Items:**", ""]
    lines.append("| Item | CoD/period | Duration | CD3 |")
    lines.append("| --- | ---: | ---: | ---: |")
    for i in items:
        cd3 = i.cod / i.duration
        lines.append(f"| {i.name} | ${i.cod:,.0f} | {i.duration} | {cd3:,.1f} |")
    lines.append("")
    return "\n".join(lines)


def format_comparison(items: list[Item], results: list[dict]) -> str:
    lines = ["**Comparison:**", ""]
    lines.append("| Order | Total revenue | Total opp cost | Opp cost saving vs worst |")
    lines.append("| --- | ---: | ---: | ---: |")
    worst_opp = max(r["total_opportunity_cost"] for r in results)
    for r in results:
        saving = worst_opp - r["total_opportunity_cost"]
        pct = (saving / worst_opp * 100) if worst_opp > 0 else 0
        order_label = " > ".join(r["order"])
        lines.append(
            f"| {order_label} | ${r['total_revenue']:,.0f} | "
            f"${r['total_opportunity_cost']:,.0f} | "
            f"${saving:,.0f} ({pct:.0f}%) |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CD3 revenue/opportunity-cost table generator")
    parser.add_argument("--items", type=str, help='Comma-separated Name:CoD:Duration (e.g. "A:1:5, B:4:1, C:5:2")')
    parser.add_argument("--json", type=str, help="Path to JSON file with items array [{name, cod, duration}]")
    parser.add_argument("--order", type=str, help='Custom order (e.g. "B,C,A"). Default: CD3 order.')
    parser.add_argument("--compare", nargs="+", help='Multiple orderings to compare (e.g. "A,B,C" "B,C,A")')
    parser.add_argument("--period-label", type=str, default="Period", help="Label for period column (Week, Month)")
    args = parser.parse_args()

    if args.json:
        with open(args.json, encoding="utf-8-sig") as f:
            data = json.load(f)
        items = [Item(name=d["name"], cod=d["cod"], duration=d["duration"]) for d in data]
    elif args.items:
        items = parse_items(args.items)
    else:
        parser.error("Provide --items or --json")
        return

    print(format_summary(items))

    if args.compare:
        results = []
        for order_str in args.compare:
            order = resolve_order(items, order_str)
            result = build_table(items, order)
            results.append(result)
            print(format_table(items, result, args.period_label))
        print(format_comparison(items, results))
    else:
        if args.order:
            order = resolve_order(items, args.order)
        else:
            order = cd3_order(items)
        result = build_table(items, order)
        print(format_table(items, result, args.period_label))


if __name__ == "__main__":
    main()
