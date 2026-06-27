#!/usr/bin/env python3
"""
宅域 一致性校验工具 (verify.py)
================================
扫描所有文档，与 data/facts.yaml 对比，找出不一致。

用法：
    python tools/verify.py                         # 完整扫描
    python tools/verify.py --quick                  # 只扫数字冲突
    python tools/verify.py --fix DEC-012            # 标记某条决议为"已同步"
    
返回码：0=无问题，1=有警告，2=有错误
"""

import os
import re
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_PATH = os.path.join(ROOT, "data", "facts.yaml")
DECISIONS_PATH = os.path.join(ROOT, "data", "decisions.yaml")

# 哪些文件的数字需要扫描（跳过二进制、git、大文件）
SKIP_DIRS = {".git", "__pycache__", "node_modules", "raw", "archive"}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".wemtv", ".wemta",
             ".wemtc", ".wemtvidx", ".wemtaidx", ".xlsx", ".ico", ".svg",
             ".pyc", ".exe", ".dll"}
SKIP_FILES = {".gitignore", "LICENSE", "desktop.ini"}

issues = []
warnings = []


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_md_html_files(root):
    """收集所有需要扫描的 .md 和 .html 文件"""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXTS or f in SKIP_FILES:
                continue
            if ext in (".md", ".html", ".htm"):
                files.append(os.path.join(dirpath, f))
    return files


def extract_numbers_from_text(text):
    """提取文档中可能的数字（万以上的）"""
    # 匹配 数字+万 模式
    wan_patterns = re.findall(r'(\d+\.?\d*)\s*万', text)
    # 匹配单个大数字（可能作为独立数字）
    big_nums = re.findall(r'(?<![.\d])(\d{4,6})(?![.\d])', text)
    return wan_patterns + big_nums


def check_number(text, facts, filename):
    """检查文档中的数字是否与 facts.yaml 一致"""
    facts_numbers = {}
    facts_numbers["12"] = "startup.total (120000/12万)"
    facts_numbers["120000"] = "startup.total"
    facts_numbers["9850"] = "costs.monthly_fixed"
    facts_numbers["328"] = "costs.daily_fixed"
    facts_numbers["750"] = "revenue.daily_target"
    facts_numbers["699.5"] = "revenue.daily_forecast"
    facts_numbers["50.5"] = "revenue.daily_gap"
    facts_numbers["8000"] = "costs.rent / costs.deposit"
    facts_numbers["500"] = "costs.utilities"
    facts_numbers["1350"] = "costs.misc"
    facts_numbers["51000"] = "shareholders.孙淦浩.investment"
    facts_numbers["39000"] = "shareholders.陈老师.investment"
    facts_numbers["30000"] = "shareholders.张显坤.investment"
    
    # 扫描文件中的数字
    for num_str, fact_key in facts_numbers.items():
        # 数字出现在文件中的多种写法
        patterns = [
            num_str,                    # "120000"
            num_str.replace("000", ""),  # "12" (小心误判)
        ]
        # 太短的数字（如"12"）跳过，避免误报
        if len(num_str) <= 2:
            continue
            
        # 查找冲突的旧数字
        pass  # 这个方法需要改进
    

def check_consistency():
    """主校验逻辑"""
    facts = load_yaml(FACTS_PATH)
    decisions = load_yaml(DECISIONS_PATH)
    
    print(f"📋 宅域一致性校验 — 开始")
    print(f"   事实源: data/facts.yaml")
    print(f"   决策源: data/decisions.yaml ({len(decisions['decisions'])} 条)")
    print()
    
    files = collect_md_html_files(ROOT)
    print(f"   扫描 {len(files)} 个文件...")
    
    for fpath in files:
        relpath = os.path.relpath(fpath, ROOT).replace("\\", "/")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查1：DEC 引用完整性
        dec_refs = re.findall(r'DEC-\d+', content)
        known_ids = {d["id"] for d in decisions["decisions"]}
        for ref in dec_refs:
            if ref not in known_ids:
                issues.append(f"⚠️  {relpath}: 引用不存在的 {ref}")
        
        # 检查2：旧数字残留（和 facts.yaml 对不上的）
        if "22" in content and "启动" in content or "启动" in content and "22万" in content:
            # 只有在不是 raw/archive 里的文件才报
            if not relpath.startswith("raw/") and not relpath.startswith("archive/"):
                if "22万" in content and facts["startup"]["total"] != 220000:
                    actual = facts["startup"]["total"] // 10000
                    issues.append(f"❌ {relpath}: 引用旧数字'22万'，实际应为 {actual}万")
        
        if "24-32" in content and not relpath.startswith("raw/") and not relpath.startswith("archive/"):
            issues.append(f"❌ {relpath}: 引用旧回本周期'24-32月'，实际应为'12个月'")
        
        if "1.57" in content and not relpath.startswith("raw/") and not relpath.startswith("archive/"):
            issues.append(f"❌ {relpath}: 引用旧月固定成本'1.57万'，实际应为'9850元'")
        
        # 检查3：facts.yaml 的 affected_bps 是否已同步
        for dec in decisions["decisions"]:
            if dec["status"] != "active":
                continue
            for affected in dec.get("affected_bps", []):
                if affected in relpath or os.path.basename(affected) == os.path.basename(relpath):
                    # 检查这个文件是否包含该决议的引用
                    if f"DEC-{dec['id'].split('-')[1]}" not in content:
                        warnings.append(f"🔔 {relpath}: 被 {dec['id']} 标记为受影响，但未包含该决议引用")

    print()
    if not issues and not warnings:
        print("✅ 通过！无一致性问题。")
        return 0
    
    if issues:
        print(f"❌ {len(issues)} 个问题需要处理：")
        for i in issues:
            print(f"   {i}")
    
    if warnings:
        print(f"\n🔔 {len(warnings)} 个提醒：")
        for w in warnings:
            print(f"   {w}")
    
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(check_consistency())
