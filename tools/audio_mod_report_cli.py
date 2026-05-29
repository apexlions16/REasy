#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from file_handlers.sound.audio_mod_report import (  # noqa: E402
    build_audio_track_report,
    export_audio_track_report_csv,
    export_audio_track_report_json,
    load_audio_name_map,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build JSON/CSV reports for REasy-supported sound banks (BNK/PCK/SBNK/SPCK)."
    )
    parser.add_argument("input", help="Input BNK/PCK/SBNK/SPCK file")
    parser.add_argument(
        "--name-map",
        help="Optional CSV/JSON/TXT source-id map with columns like source_id,name,dialogue_text,character",
    )
    parser.add_argument("--json", dest="json_out", help="Output JSON report path")
    parser.add_argument("--csv", dest="csv_out", help="Output CSV report path")
    parser.add_argument(
        "--out-dir",
        help="Output directory. If --json/--csv are omitted, both reports are created here.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    try:
        data = input_path.read_bytes()
    except OSError as exc:
        print(f"Failed to read input file: {exc}", file=sys.stderr)
        return 2

    name_map = None
    if args.name_map:
        try:
            name_map = load_audio_name_map(args.name_map)
        except Exception as exc:
            print(f"Failed to load name map: {exc}", file=sys.stderr)
            return 2

    try:
        report = build_audio_track_report(data, name_map=name_map)
    except Exception as exc:
        print(f"Failed to parse sound bank: {exc}", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir) if args.out_dir else input_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = input_path.name.replace(".", "_")

    json_out = Path(args.json_out) if args.json_out else out_dir / f"{base_name}_audio_report.json"
    csv_out = Path(args.csv_out) if args.csv_out else out_dir / f"{base_name}_audio_report.csv"

    try:
        export_audio_track_report_json(report, json_out)
        export_audio_track_report_csv(report, csv_out)
    except OSError as exc:
        print(f"Failed to write report: {exc}", file=sys.stderr)
        return 2

    print(f"Container: {str(report.get('container_type', '')).upper()}")
    print(f"Tracks: {report.get('track_count', 0)}")
    print(f"JSON: {json_out}")
    print(f"CSV: {csv_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
