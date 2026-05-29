from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .bnk_parser import extract_embedded_wem, parse_soundbank, parse_wem_metadata


@dataclass(slots=True)
class AudioTrackReportRow:
    index: int
    source_id: int
    name: str | None
    dialogue_text: str | None
    offset: int
    length: int
    absolute_offset: bool
    embedded: bool
    duration_seconds: float | None
    codec: str
    channels: int | None
    sample_rate: int | None
    suggested_wem_filename: str
    suggested_wav_filename: str
    notes: str


def _norm_id(value: Any) -> str:
    return str(value).strip()


def load_audio_name_map(path: str | Path) -> dict[str, dict[str, str]]:
    """
    Load an optional source-id/name/dialogue map for audio banks.

    Supported lightweight formats:
    - JSON dict: {"12345": "name"} or {"12345": {"name": "...", "dialogue_text": "..."}}
    - JSON list: [{"source_id": 12345, "name": "...", "dialogue_text": "..."}]
    - CSV: columns such as source_id/id, name/event_name, dialogue_text/text/line
    - TXT: lines like `12345=event_name` or `12345 event_name`

    This deliberately stays simple. Later phases can add SoundbanksInfo.xml,
    Wwise_IDs.h, wwnames.txt/db3 and subtitle/MSG fuzzy matching parsers.
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(str(p))

    suffix = p.suffix.lower()
    if suffix == ".json":
        return _load_json_name_map(p)
    if suffix == ".csv":
        return _load_csv_name_map(p)
    return _load_txt_name_map(p)


def _coerce_map_entry(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        out: dict[str, str] = {}
        for key in ("name", "event_name", "object_name", "dialogue_text", "text", "line", "character"):
            if value.get(key) not in (None, ""):
                target = "dialogue_text" if key in {"text", "line"} else key
                if target == "event_name" or target == "object_name":
                    target = "name"
                out[target] = str(value[key])
        return out
    return {"name": str(value)} if value not in (None, "") else {}


def _load_json_name_map(path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, str]] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            entry = _coerce_map_entry(value)
            if entry:
                result[_norm_id(key)] = entry
    elif isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            source_id = item.get("source_id", item.get("id", item.get("wem_id")))
            if source_id in (None, ""):
                continue
            entry = _coerce_map_entry(item)
            if entry:
                result[_norm_id(source_id)] = entry
    else:
        raise ValueError("Unsupported JSON name map structure")
    return result


def _first_present(row: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    lowered = {str(k).lower(): v for k, v in row.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return str(value).strip()
    return None


def _load_csv_name_map(path: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_id = _first_present(row, ("source_id", "id", "wem_id", "source", "short_id"))
            if not source_id:
                continue
            entry: dict[str, str] = {}
            name = _first_present(row, ("name", "event_name", "object_name", "audio_name"))
            text = _first_present(row, ("dialogue_text", "text", "line", "subtitle", "tr_text"))
            character = _first_present(row, ("character", "speaker", "actor"))
            if name:
                entry["name"] = name
            if text:
                entry["dialogue_text"] = text
            if character:
                entry["character"] = character
            if entry:
                result[_norm_id(source_id)] = entry
    return result


def _load_txt_name_map(path: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            left, right = line.split("=", 1)
        elif "," in line:
            left, right = line.split(",", 1)
        else:
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            left, right = parts
        source_id, name = left.strip(), right.strip()
        if source_id and name:
            result[_norm_id(source_id)] = {"name": name}
    return result


def build_audio_track_report(
    data: bytes,
    *,
    name_map: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Build a structured report for BNK/PCK/SBNK/SPCK-like sound containers."""
    parsed = parse_soundbank(data)
    rows: list[AudioTrackReportRow] = []
    name_map = name_map or {}

    for track in parsed.tracks:
        wem_data = extract_embedded_wem(data, track)
        meta = parse_wem_metadata(wem_data) if wem_data else None
        mapped = name_map.get(_norm_id(track.source_id), {})
        notes: list[str] = []
        if not wem_data:
            notes.append("No embedded WEM data found; check external/streaming bank references.")
        if meta and meta.duration_seconds is None:
            notes.append("Duration could not be calculated from RIFF metadata.")
        if meta and meta.codec == "Unknown":
            notes.append("Codec could not be identified from WEM metadata.")

        rows.append(
            AudioTrackReportRow(
                index=int(track.index),
                source_id=int(track.source_id),
                name=mapped.get("name"),
                dialogue_text=mapped.get("dialogue_text"),
                offset=int(track.offset),
                length=int(track.length),
                absolute_offset=bool(track.absolute_offset),
                embedded=bool(wem_data),
                duration_seconds=meta.duration_seconds if meta else None,
                codec=meta.codec if meta else "Unknown",
                channels=meta.channels if meta else None,
                sample_rate=meta.sample_rate if meta else None,
                suggested_wem_filename=f"{track.source_id}.wem",
                suggested_wav_filename=f"{track.source_id}.wav",
                notes=" ".join(notes),
            )
        )

    return {
        "container_type": parsed.container_type,
        "bank_version": parsed.bank_version,
        "has_embedded_data": parsed.has_embedded_data,
        "track_count": len(rows),
        "tracks": [asdict(row) for row in rows],
    }


def export_audio_track_report_json(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def export_audio_track_report_csv(report: dict[str, Any], path: str | Path) -> None:
    tracks = list(report.get("tracks") or [])
    fieldnames = [
        "index",
        "source_id",
        "name",
        "dialogue_text",
        "offset",
        "length",
        "absolute_offset",
        "embedded",
        "duration_seconds",
        "codec",
        "channels",
        "sample_rate",
        "suggested_wem_filename",
        "suggested_wav_filename",
        "notes",
    ]
    with Path(path).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in tracks:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
