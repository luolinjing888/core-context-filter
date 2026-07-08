#!/usr/bin/env python3
"""Create a first-pass core-context handoff packet from a local text file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SIGNAL_PATTERNS = [
    r"\bmust\b|\bshould\b|\brequired\b|\bcritical\b|\brisk\b|\bblocker\b",
    r"\bstep\b|\bworkflow\b|\bprocess\b|\bSOP\b|\bchecklist\b",
    r"\bmetric\b|\bKPI\b|\bbenchmark\b|\bconversion\b|\bpricing\b|\bcost\b",
    r"\bAPI\b|\bschema\b|\bcommand\b|\berror\b|\bfailure\b|\bbug\b",
    r"必须|应该|关键|风险|阻塞|步骤|流程|指标|成本|价格|错误|失败|验收|标准",
]


def split_units(text: str) -> list[str]:
    blocks = re.split(r"\n\s*\n+", text.strip())
    units: list[str] = []
    for block in blocks:
        block = re.sub(r"\s+", " ", block).strip()
        if not block:
            continue
        if len(block) <= 700:
            units.append(block)
        else:
            parts = re.split(r"(?<=[.!?。！？])\s+", block)
            units.extend(p.strip() for p in parts if p.strip())
    return units


def score_unit(unit: str) -> int:
    score = 0
    for pattern in SIGNAL_PATTERNS:
        if re.search(pattern, unit, flags=re.I):
            score += 2
    if re.search(r"https?://|www\.", unit):
        score += 1
    if re.search(r"\d+[%$]?|\bQ[1-4]\b|\b20\d{2}\b", unit):
        score += 1
    if len(unit) > 500:
        score -= 1
    return score


def trim(unit: str, limit: int = 360) -> str:
    if len(unit) <= limit:
        return unit
    return unit[: limit - 1].rstrip() + "..."


def build_packet(text: str, agent: str, task: str, source: str, max_items: int) -> str:
    units = split_units(text)
    ranked = sorted(enumerate(units, start=1), key=lambda item: score_unit(item[1]), reverse=True)
    keep = [(idx, unit) for idx, unit in ranked if score_unit(unit) > 0][:max_items]
    deferred = [(idx, unit) for idx, unit in ranked if score_unit(unit) <= 0][: min(5, max_items)]

    lines = [
        "# Core Context Handoff",
        "",
        "## Intended Agent",
        f"- Role: {agent}",
        f"- Task: {task}",
        f"- Source: {source}",
        "",
        "## Core Context",
    ]
    if keep:
        for _, unit in keep:
            lines.append(f"- {trim(unit)}")
    else:
        lines.append("- No high-signal units detected automatically. Review the source manually.")

    lines.extend(["", "## Execution Implications"])
    for _, unit in keep[: min(5, len(keep))]:
        lines.append(f"- Consider this during execution: {trim(unit, 220)}")
    if not keep:
        lines.append("- Manual review required before handoff.")

    lines.extend([
        "",
        "## Reference Map",
        "| Core point | Source reference | Why it matters |",
        "|---|---|---|",
    ])
    for idx, unit in keep:
        lines.append(f"| {trim(unit, 120)} | unit {idx} | Potentially changes execution or validation. |")

    lines.extend(["", "## Discarded / Deferred Context", "- Deferred:"])
    if deferred:
        for idx, unit in deferred:
            lines.append(f"  - unit {idx}: {trim(unit, 180)}")
    else:
        lines.append("  - None identified automatically.")
    lines.append("- Dropped: repetitive, promotional, or low-signal material not listed above.")

    lines.extend([
        "",
        "## Uncertainty / Follow-Up",
        "- This is an automatic first pass; verify claims and source reliability before acting.",
        "- Preserve the raw source for fallback inspection.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Text or Markdown source file")
    parser.add_argument("--agent", default="unspecified agent")
    parser.add_argument("--task", default="extract task-ready core context")
    parser.add_argument("--out", default="")
    parser.add_argument("--max-items", type=int, default=12)
    args = parser.parse_args()

    source = Path(args.input)
    text = source.read_text(encoding="utf-8", errors="replace")
    packet = build_packet(text, args.agent, args.task, str(source), args.max_items)
    if args.out:
        Path(args.out).write_text(packet, encoding="utf-8")
    else:
        print(packet, end="")


if __name__ == "__main__":
    main()
