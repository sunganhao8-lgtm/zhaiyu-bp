#!/usr/bin/env python3
"""
Zhaiyu consistency check.

Return codes:
  0 = OK
  1 = warnings only
  2 = errors
"""

import os
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FACTS_PATH = ROOT / "data" / "facts.yaml"
DECISIONS_PATH = ROOT / "data" / "decisions.yaml"
BP_PATH = ROOT / "bp.html"

SKIP_DIRS = {".git", "__pycache__", "node_modules", "raw", "archive", "assets"}
SKIP_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".mp4",
    ".wemtv",
    ".wemta",
    ".wemtc",
    ".wemtvidx",
    ".wemtaidx",
    ".xlsx",
    ".ico",
    ".svg",
    ".pyc",
    ".exe",
    ".dll",
}

EXPECTED = {
    "startup_total": 182300,
    "monthly_fixed": 6416,
    "rent": 3233,
    "utilities": 800,
    "staff_base": 1500,
    "misc": 880,
    "deposit": 8000,
    "daily_fixed": 213.87,
    "rent_annual_nominal": 38800,
    "rent_annual_actual": 32300,
    "area_sqm": 59.87,
    "transfer_fee": 0,
    "renovation_budget": 40000,
    "monthly_net_profit_phase0": 4974,
    "monthly_net_profit_m6": 5584,
    "monthly_net_profit_m12": 8584,
    "monthly_net_profit_m24": 10084,
    "investments": [64000, 59000, 59000, 0],
    "equities": [0.325, 0.2875, 0.2875, 0.10],
    "capital_pool": 0.70,
    "human_capital_pool": 0.30,
}

BP_REQUIRED_SNIPPETS = [
    "18.23 万元",
    "59.87㎡",
    "3233",
    "约 6416",
    "12-18 个月",
    "+4974",
    "+5584",
    "+8584",
    "+10084",
    "32.5%",
    "28.75%",
    "装修签约控制价",
    "6.70",
    "无原店转让费",
]


def load_yaml(path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def approx_equal(actual, expected, epsilon=0.001):
    return abs(float(actual) - float(expected)) <= epsilon


def collect_text_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in SKIP_EXTS:
                continue
            if path.suffix.lower() in {".md", ".html", ".htm"}:
                files.append(path)
    return files


def check_facts(facts, errors):
    startup = facts["startup"]
    costs = facts["costs"]
    revenue = facts["revenue"]
    store = facts["store"]
    shareholders = facts["shareholders"]

    scalar_checks = [
        ("startup.total", startup["total"], EXPECTED["startup_total"]),
        ("costs.monthly_fixed", costs["monthly_fixed"], EXPECTED["monthly_fixed"]),
        ("costs.rent", costs["rent"], EXPECTED["rent"]),
        ("costs.utilities", costs["utilities"], EXPECTED["utilities"]),
        ("costs.staff_base", costs["staff_base"], EXPECTED["staff_base"]),
        ("costs.misc", costs["misc"], EXPECTED["misc"]),
        ("costs.deposit", costs["deposit"], EXPECTED["deposit"]),
        ("costs.daily_fixed", costs["daily_fixed"], EXPECTED["daily_fixed"]),
        ("costs.rent_annual_nominal", costs["rent_annual_nominal"], EXPECTED["rent_annual_nominal"]),
        ("costs.rent_annual_actual", costs["rent_annual_actual"], EXPECTED["rent_annual_actual"]),
        ("store.area_sqm", store["area_sqm"], EXPECTED["area_sqm"]),
        ("store.transfer_fee", store["transfer_fee"], EXPECTED["transfer_fee"]),
        ("store.renovation_budget", store["renovation_budget"], EXPECTED["renovation_budget"]),
        ("revenue.monthly_net_profit_phase0", revenue["monthly_net_profit_phase0"], EXPECTED["monthly_net_profit_phase0"]),
        ("revenue.monthly_net_profit_m6", revenue["monthly_net_profit_m6"], EXPECTED["monthly_net_profit_m6"]),
        ("revenue.monthly_net_profit_m12", revenue["monthly_net_profit_m12"], EXPECTED["monthly_net_profit_m12"]),
        ("revenue.monthly_net_profit_m24", revenue["monthly_net_profit_m24"], EXPECTED["monthly_net_profit_m24"]),
    ]

    for label, actual, expected in scalar_checks:
        if not approx_equal(actual, expected):
            errors.append(f"{label}: expected {expected}, got {actual}")

    investments = [s.get("investment", 0) for s in shareholders]
    equities = [s.get("equity", 0) for s in shareholders]
    if investments != EXPECTED["investments"]:
        errors.append(f"shareholders.investment: expected {EXPECTED['investments']}, got {investments}")
    if not all(approx_equal(a, e) for a, e in zip(equities, EXPECTED["equities"])):
        errors.append(f"shareholders.equity: expected {EXPECTED['equities']}, got {equities}")

    investment_total = sum(investments)
    startup_adjustment = startup.get("rounding_adjustment", 0)
    if investment_total + startup_adjustment != EXPECTED["startup_total"]:
        errors.append(
            "startup.total must equal shareholder investment total plus explicit adjustment: "
            f"{EXPECTED['startup_total']} != {investment_total} + {startup_adjustment}"
        )
    if startup.get("shareholder_investment_total") != investment_total:
        errors.append(f"startup.shareholder_investment_total must be {investment_total}")

    if not approx_equal(sum(equities), 1.0):
        errors.append(f"shareholders.equity must sum to 100%, got {sum(equities):.4f}")
    if not approx_equal(EXPECTED["capital_pool"] + EXPECTED["human_capital_pool"], 1.0):
        errors.append("dual-track pool must be capital 70% + human capital 30% = 100%")

    if facts.get("shareholders_legacy", {}).get("superseded_by") != "DEC-029":
        errors.append("shareholders_legacy.superseded_by must be DEC-029")
    if facts.get("storefront_area_legacy_49sqm", {}).get("superseded_by") is None:
        errors.append("storefront_area_legacy_49sqm must be marked superseded")


def check_decisions(decisions, errors):
    by_id = {d["id"]: d for d in decisions["decisions"]}
    if "DEC-029" not in by_id:
        errors.append("data/decisions.yaml missing DEC-029")
        return

    if by_id["DEC-029"].get("status") != "active":
        errors.append("DEC-029 must be active")
    if "DEC-032" not in by_id or by_id["DEC-032"].get("status") != "active":
        errors.append("DEC-032 must exist and be active")
    dec_031 = by_id.get("DEC-031")
    if not dec_031 or dec_031.get("status") != "superseded" or dec_031.get("superseded_by") != "DEC-032":
        errors.append("DEC-031 must be superseded by DEC-032")
    for old_id in ["DEC-012", "DEC-014", "DEC-024"]:
        dec = by_id.get(old_id)
        if not dec:
            errors.append(f"missing historical {old_id}")
            continue
        if dec.get("status") != "superseded" or dec.get("superseded_by") != "DEC-029":
            errors.append(f"{old_id} must be superseded by DEC-029")


def check_bp_html(errors, warnings):
    html = BP_PATH.read_text(encoding="utf-8")
    for snippet in BP_REQUIRED_SNIPPETS:
        if snippet not in html:
            errors.append(f"bp.html missing current snippet: {snippet}")

    forbidden_patterns = [
        (r"49㎡|49\s*平方米", "49㎡ old area"),
        (r"120000", "120000 old startup total"),
        (r"9850", "9850 old monthly fixed cost"),
    ]
    for pattern, label in forbidden_patterns:
        if re.search(pattern, html):
            errors.append(f"bp.html contains {label}")

    for match in re.finditer(r"(?<!\d)8000(?!\d)", html):
        context = html[max(0, match.start() - 60) : match.end() + 60]
        if "押金" not in context and "6000-8000" not in context and "5500-8000" not in context:
            errors.append("bp.html contains 8000 outside allowed deposit/profit-range context")
            break

    if "6413" in html:
        warnings.append("bp.html explains 3233 + 800 + 1500 + 880 = 6413 while headline says 6416")


# ── DEC-035 v5 设备对比口径（2026-08-07 霍曼新样机价后重算） ──
# 数字唯一来源 = data/facts.yaml 的 devices_v5 段；本函数做算术自检 + 三页同步校验：
# accessories-v5.html / accessories-v5-pictures.html / bp.html（v2→v5 五次口径漂移的教训）。
DEVICE_V5_PAGES = ["accessories-v5.html", "accessories-v5-pictures.html", "bp.html"]


def check_device_v5(facts, errors):
    devices = facts.get("devices_v5")
    if not devices:
        errors.append("facts.yaml missing devices_v5 section")
        return

    segments = devices.get("segments", [])
    seg_alt = sum(s["alt_price"] for s in segments)
    seg_sample = sum(s["huoman_sample"] for s in segments)
    seg_quote = sum(s["huoman_quote"] for s in segments)
    if seg_alt != devices["alt_total"]:
        errors.append(f"devices_v5: segment alt_price sum {seg_alt} != alt_total {devices['alt_total']}")
    if seg_sample != devices["huoman_sample_total"]:
        errors.append(f"devices_v5: segment huoman_sample sum {seg_sample} != huoman_sample_total {devices['huoman_sample_total']}")
    if seg_quote != devices["huoman_original_total"]:
        errors.append(f"devices_v5: segment huoman_quote sum {seg_quote} != huoman_original_total {devices['huoman_original_total']}")
    if devices["huoman_sample_total"] - devices["alt_total"] != devices["savings"]:
        errors.append("devices_v5: huoman_sample_total - alt_total != savings")

    snippets = [
        f"¥{devices['huoman_sample_total']:,}",
        f"¥{devices['alt_total']:,}",
        f"¥{devices['savings']:,}",
        f"{devices['discount_pct']}%",
    ]
    for name in DEVICE_V5_PAGES:
        path = ROOT / name
        if not path.exists():
            errors.append(f"missing device comparison page: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{name} missing DEC-035 v5 snippet: {snippet}")
    accessory = (ROOT / "accessories-v5.html").read_text(encoding="utf-8")
    for segment in segments:
        price = f"¥{segment['alt_price']:,}"
        if price not in accessory:
            errors.append(f"accessories-v5.html missing v5 segment {segment['seg']} price: {price}")


def check_text_dec_refs(decisions, warnings):
    known_ids = {d["id"] for d in decisions["decisions"]}
    for path in collect_text_files(ROOT):
        relpath = path.relative_to(ROOT).as_posix()
        if relpath == "bp.html":
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for ref in sorted(set(re.findall(r"DEC-\d+", content))):
            if ref not in known_ids:
                warnings.append(f"{relpath}: references unknown {ref}")


def main():
    errors = []
    warnings = []

    facts = load_yaml(FACTS_PATH)
    decisions = load_yaml(DECISIONS_PATH)

    print("Zhaiyu consistency check - start")
    print("   facts: data/facts.yaml")
    print(f"   decisions: data/decisions.yaml ({len(decisions['decisions'])} entries)")
    print()

    check_facts(facts, errors)
    check_decisions(decisions, errors)
    check_bp_html(errors, warnings)
    check_device_v5(facts, errors)
    check_text_dec_refs(decisions, warnings)

    if errors:
        print(f"ERROR: {len(errors)} issue(s)")
        for error in errors:
            print(f"   ERROR {error}")
    if warnings:
        print(f"WARNING: {len(warnings)} warning(s)")
        for warning in warnings:
            print(f"   WARN {warning}")

    if errors:
        return 2
    if warnings:
        return 1

    print("OK: no consistency issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
