#!/usr/bin/env python3
"""Compact, reusable KiCad pre-fabrication checker.

The engine contains generic KiCad/layout checks.  Optional project-specific
expectations and electrical assumptions come from one JSON profile.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import pcbnew  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "error: pcbnew is unavailable; use the Python shipped with KiCad "
        "(on Debian/Ubuntu, /usr/bin/python3)"
    ) from exc


STATUS_ORDER = {"PASS": 0, "WARNING": 1, "BLOCKING": 2}
COPPER_RESISTIVITY_OHM_M = 1.724e-8
BOLTZMANN_J_K = 1.380649e-23
LIGHT_M_S = 299_792_458.0


@dataclass(frozen=True)
class Result:
    category: str
    status: str
    message: str


@dataclass(frozen=True)
class Segment:
    net: str
    layer: str
    start: tuple[float, float]
    end: tuple[float, float]
    width_mm: float
    length_mm: float


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, check=False
    )


def mm(value: int) -> float:
    return float(pcbnew.ToMM(value))


def normalized_net(name: str) -> str:
    return name.lstrip("/")


def point_segment_distance(
    point: tuple[float, float],
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    px, py = point
    ax, ay = start
    bx, by = end
    dx, dy = bx - ax, by - ay
    if dx == 0.0 and dy == 0.0:
        return math.hypot(px - ax, py - ay)
    u = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx**2 + dy**2)))
    return math.hypot(px - (ax + u * dx), py - (ay + u * dy))


def segment_distance(first: Segment, second: Segment) -> float:
    center_distance = min(
        point_segment_distance(first.start, second.start, second.end),
        point_segment_distance(first.end, second.start, second.end),
        point_segment_distance(second.start, first.start, first.end),
        point_segment_distance(second.end, first.start, first.end),
    )
    return max(0.0, center_distance - (first.width_mm + second.width_mm) / 2.0)


def microstrip(width_mm: float, height_mm: float, epsilon_r: float) -> tuple[float, float]:
    """Return approximate zero-thickness Z0 (ohm) and delay (ps/mm)."""
    ratio = width_mm / height_mm
    epsilon_eff = (epsilon_r + 1.0) / 2.0 + (epsilon_r - 1.0) / 2.0 * (
        1.0 / math.sqrt(1.0 + 12.0 / ratio)
        + (0.04 * (1.0 - ratio) ** 2 if ratio < 1.0 else 0.0)
    )
    if ratio <= 1.0:
        impedance = 60.0 / math.sqrt(epsilon_eff) * math.log(
            8.0 / ratio + 0.25 * ratio
        )
    else:
        impedance = 120.0 * math.pi / (
            math.sqrt(epsilon_eff)
            * (ratio + 1.393 + 0.667 * math.log(ratio + 1.444))
        )
    delay_ps_mm = math.sqrt(epsilon_eff) / LIGHT_M_S * 1.0e9
    return impedance, delay_ps_mm


def load_profile(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open(encoding="utf-8") as stream:
        profile = json.load(stream)
    if profile.get("schema") != 1:
        raise ValueError(f"{path}: expected profile schema 1")
    return profile


def copy_project(source_base: Path, destination: Path) -> Path:
    destination.mkdir(parents=True)
    for suffix in (".kicad_pcb", ".kicad_sch", ".kicad_pro", ".kicad_dru"):
        source = source_base.with_suffix(suffix)
        if source.exists():
            shutil.copy2(source, destination / source.name)
    for filename in ("fp-lib-table", "sym-lib-table"):
        source = source_base.parent / filename
        if source.exists():
            shutil.copy2(source, destination / filename)
            table_text = source.read_text(encoding="utf-8")
            for uri in re.findall(r'\(uri\s+"([^"]+)"\)', table_text):
                prefix = "${KIPRJMOD}/"
                if not uri.startswith(prefix):
                    continue
                relative = Path(uri[len(prefix) :])
                library_source = (source_base.parent / relative).resolve()
                library_destination = (destination / relative).resolve()
                if (
                    not library_destination.is_relative_to(destination.parent.resolve())
                    or not library_source.exists()
                    or library_destination.exists()
                ):
                    continue
                library_destination.parent.mkdir(parents=True, exist_ok=True)
                if library_source.is_dir():
                    shutil.copytree(library_source, library_destination)
                else:
                    shutil.copy2(library_source, library_destination)
    for source in source_base.parent.iterdir():
        if source.is_dir() and source.name.endswith(".pretty"):
            target = destination / source.name
            if not target.exists():
                shutil.copytree(source, target)
        elif source.is_file() and source.suffix == ".kicad_sym":
            target = destination / source.name
            if not target.exists():
                shutil.copy2(source, target)
    return destination / source_base.with_suffix(".kicad_pcb").name


def schematic_components(kicad_cli: str, schematic: Path, temporary: Path) -> list[dict[str, str]]:
    output = temporary / f"{schematic.stem}-netlist.xml"
    completed = run(
        [kicad_cli, "sch", "export", "netlist", "--format", "kicadxml", "-o", str(output), str(schematic)],
        schematic.parent,
    )
    if completed.returncode != 0 or not output.exists():
        return []
    root = ET.parse(output).getroot()
    return [
        {
            "ref": component.get("ref", ""),
            "value": component.findtext("value", ""),
            "footprint": component.findtext("footprint", ""),
        }
        for component in root.findall("./components/comp")
    ]


def json_findings(document: dict[str, Any], key: str) -> list[dict[str, Any]]:
    if key == "erc":
        return [
            violation
            for sheet in document.get("sheets", [])
            for violation in sheet.get("violations", [])
        ]
    return list(document.get(key, []))


def unique_messages(findings: Iterable[dict[str, Any]]) -> list[str]:
    messages = []
    for finding in findings:
        message = f"{finding.get('type', 'unknown')}: {finding.get('description', 'no description')}"
        items = sorted(
            {
                item.get("description", "")
                for item in finding.get("items", [])
                if item.get("description")
            }
        )
        if items:
            message += " [" + " / ".join(items) + "]"
        messages.append(message)
    counts: collections.Counter[str] = collections.Counter(messages)
    return [f"{message} ({count}x)" if count > 1 else message for message, count in sorted(counts.items())]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="project base path, without KiCad suffix")
    parser.add_argument("--profile", type=Path, help="optional project validation JSON")
    parser.add_argument("--output", type=Path, default=Path("build/checks"))
    arguments = parser.parse_args()

    root = Path.cwd().resolve()
    base = (root / arguments.project).resolve() if not arguments.project.is_absolute() else arguments.project.resolve()
    profile_path = None
    if arguments.profile:
        profile_path = (root / arguments.profile).resolve() if not arguments.profile.is_absolute() else arguments.profile.resolve()
    output_dir = (root / arguments.output).resolve() if not arguments.output.is_absolute() else arguments.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{base.name}-report.md"
    results: list[Result] = []
    tables: dict[str, Any] = {}

    def record(category: str, status: str, message: str) -> None:
        results.append(Result(category, status, message))

    try:
        profile = load_profile(profile_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report_path.write_text(f"# KiCad validation\n\nBLOCKING: invalid profile: {exc}\n", encoding="utf-8")
        print(f"BLOCKING: invalid profile: {exc}", file=sys.stderr)
        return 2

    locked_version = profile.get("locked_kicad")
    kicad_cli = shutil.which("kicad-cli")
    if kicad_cli is None:
        record("toolchain", "BLOCKING", "kicad-cli is required")
    else:
        version = run([kicad_cli, "version"], root).stdout.strip()
        version_ok = locked_version is None or version.startswith(str(locked_version))
        required_text = f"; required {locked_version}" if locked_version else ""
        record("toolchain", "PASS" if version_ok else "BLOCKING", f"KiCad {version or 'unknown'}{required_text}")

    required = [base.with_suffix(suffix) for suffix in (".kicad_pro", ".kicad_sch", ".kicad_pcb")]
    missing = [str(path) for path in required if not path.is_file()]
    record("source", "BLOCKING" if missing else "PASS", f"Missing: {', '.join(missing)}" if missing else "Project, schematic, and PCB are present")
    rule_file = base.with_suffix(".kicad_dru")
    if profile.get("require_custom_rules", False):
        record("source", "PASS" if rule_file.is_file() else "BLOCKING", f"Custom rules: {rule_file}")
        if rule_file.is_file():
            rule_text = rule_file.read_text(encoding="utf-8")
            missing_patterns = [
                pattern
                for pattern in profile.get("required_rule_patterns", [])
                if re.search(str(pattern), rule_text, re.MULTILINE) is None
            ]
            record(
                "custom rules",
                "BLOCKING" if missing_patterns else "PASS",
                f"Missing configured patterns: {missing_patterns}"
                if missing_patterns
                else "Configured custom-rule patterns are present",
            )
    if missing or kicad_cli is None:
        write_report(report_path, base, profile_path, results, tables)
        return 2

    source_pcb = base.with_suffix(".kicad_pcb")
    source_schematic = base.with_suffix(".kicad_sch")
    source_text = source_pcb.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(source_pcb.read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="kicad-check-") as temporary_name:
        temporary = Path(temporary_name)
        working_pcb = copy_project(base, temporary / base.parent.name)
        board = pcbnew.LoadBoard(str(working_pcb))
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
        pcbnew.SaveBoard(str(working_pcb), board)

        erc_path = temporary / "erc.json"
        erc_run = run(
            [kicad_cli, "sch", "erc", "--format", "json", "--severity-all", "--severity-exclusions", "-o", str(erc_path), str(source_schematic)],
            base.parent,
        )
        if erc_run.returncode != 0 or not erc_path.exists():
            record("ERC", "BLOCKING", (erc_run.stderr or erc_run.stdout or "ERC produced no report").strip())
            erc = {}
        else:
            erc = json.loads(erc_path.read_text(encoding="utf-8"))
            violations = json_findings(erc, "erc")
            exclusions = [item for item in violations if item.get("severity") == "exclusion"]
            serious = [item for item in violations if item.get("severity") == "error" or item.get("type") == "lib_symbol_issues"]
            warnings = [item for item in violations if item not in serious and item not in exclusions]
            if serious or exclusions:
                status = "BLOCKING"
            elif warnings:
                status = "WARNING"
            else:
                status = "PASS"
            detail = "; ".join(unique_messages(violations)) or "No findings"
            record("ERC", status, detail)

        drc_path = temporary / "drc.json"
        drc_run = run(
            [kicad_cli, "pcb", "drc", "--format", "json", "--severity-all", "--severity-exclusions", "--schematic-parity", "-o", str(drc_path), str(working_pcb)],
            working_pcb.parent,
        )
        if drc_run.returncode != 0 or not drc_path.exists():
            record("DRC", "BLOCKING", (drc_run.stderr or drc_run.stdout or "DRC produced no report").strip())
            drc = {}
        else:
            drc = json.loads(drc_path.read_text(encoding="utf-8"))
            drc_violations = json_findings(drc, "violations")
            unconnected = json_findings(drc, "unconnected_items")
            parity = json_findings(drc, "schematic_parity")
            exclusions = [item for item in drc_violations if item.get("severity") == "exclusion"]
            errors = [item for item in drc_violations if item.get("severity") == "error"]
            warnings = [item for item in drc_violations if item.get("severity") == "warning"]
            status = "BLOCKING" if errors or exclusions or unconnected or parity else ("WARNING" if warnings else "PASS")
            detail_parts = unique_messages(drc_violations)
            detail_parts += [f"unconnected: {message}" for message in unique_messages(unconnected)]
            detail_parts += [f"parity: {message}" for message in unique_messages(parity)]
            record("DRC/parity", status, "; ".join(detail_parts) or "No findings after temporary zone refill")
            tables["drc_counts"] = {
                "violations": len(drc_violations),
                "unconnected": len(unconnected),
                "parity": len(parity),
                "exclusions": len(exclusions),
            }

        components = schematic_components(kicad_cli, source_schematic, temporary)
        power_components: list[dict[str, str]] = []
        power_base_text = profile.get("related_power_project")
        if power_base_text:
            power_base = (root / power_base_text).resolve()
            power_schematic = power_base.with_suffix(".kicad_sch")
            if power_schematic.exists():
                power_components = schematic_components(kicad_cli, power_schematic, temporary)
            else:
                record("related project", "BLOCKING", f"Missing related schematic {power_schematic}")

        analyze_board(board, source_text, profile, components, power_components, record, tables)
        run_simulations(profile, root, temporary, record, tables)

        fab_dir = temporary / "fab"
        fab_dir.mkdir()
        gerber = run(
            [kicad_cli, "pcb", "export", "gerbers", "--layers", "F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts", "--output", str(fab_dir), str(working_pcb)],
            working_pcb.parent,
        )
        drill = run(
            [kicad_cli, "pcb", "export", "drill", "--excellon-separate-th", "--output", str(fab_dir), str(working_pcb)],
            working_pcb.parent,
        )
        fab_files = [path for path in fab_dir.iterdir() if path.is_file() and path.stat().st_size > 0]
        outline_box = board.GetBoardEdgesBoundingBox()
        source_has_outline = mm(outline_box.GetWidth()) > 0.1 and mm(outline_box.GetHeight()) > 0.1
        has_edge = source_has_outline and any("Edge_Cuts" in path.name for path in fab_files)
        has_drill = any(path.suffix == ".drl" for path in fab_files)
        fab_ok = gerber.returncode == 0 and drill.returncode == 0 and has_edge and has_drill
        record("fabrication smoke test", "PASS" if fab_ok else "BLOCKING", f"Generated {len(fab_files)} nonempty temporary files; edge={has_edge}, drill={has_drill}")

        render_paths = []
        for side in ("top", "bottom"):
            render_path = output_dir / f"{base.name}-{side}.png"
            rendered = run(
                [kicad_cli, "pcb", "render", "--side", side, "--quality", "basic", "--output", str(render_path), str(working_pcb)],
                working_pcb.parent,
            )
            if rendered.returncode == 0 and render_path.exists() and render_path.stat().st_size > 0:
                render_paths.append(render_path)
        record("board renders", "PASS" if len(render_paths) == 2 else "WARNING", f"Generated {len(render_paths)}/2 review images; visual review is still required")

    tables["source_hash"] = source_hash
    write_report(report_path, base, profile_path, results, tables)
    blocking = sum(result.status == "BLOCKING" for result in results)
    warning = sum(result.status == "WARNING" for result in results)
    print(f"{base.name}: {blocking} blocking, {warning} warning; report: {report_path}")
    return 1 if blocking else 0


def analyze_board(
    board: Any,
    source_text: str,
    profile: dict[str, Any],
    components: list[dict[str, str]],
    power_components: list[dict[str, str]],
    record: Any,
    tables: dict[str, Any],
) -> None:
    footprints = list(board.GetFootprints())
    references = [footprint.GetReference() for footprint in footprints]
    duplicate_refs = sorted(ref for ref, count in collections.Counter(references).items() if count > 1)
    bad_refs = sorted(ref for ref in references if not ref or ref == "REF**")
    record("references", "BLOCKING" if duplicate_refs or bad_refs else "PASS", f"duplicates={duplicate_refs or 'none'}, invalid={bad_refs or 'none'}")

    segments: list[Segment] = []
    vias: list[Any] = []
    for item in board.GetTracks():
        if isinstance(item, pcbnew.PCB_VIA):
            vias.append(item)
            continue
        start, end = item.GetStart(), item.GetEnd()
        segments.append(
            Segment(
                item.GetNetname(),
                item.GetLayerName(),
                (mm(start.x), mm(start.y)),
                (mm(end.x), mm(end.y)),
                mm(item.GetWidth()),
                mm(item.GetLength()),
            )
        )
    lengths: dict[str, float] = collections.defaultdict(float)
    layer_lengths: dict[str, float] = collections.defaultdict(float)
    widths: collections.Counter[float] = collections.Counter()
    for segment in segments:
        lengths[segment.net] += segment.length_mm
        layer_lengths[segment.layer] += segment.length_mm
        widths[segment.width_mm] += 1
    tables["inventory"] = {
        "footprints": len(footprints),
        "segments": len(segments),
        "vias": len(vias),
        "zones": board.GetAreaCount(),
        "tracks_by_layer_mm": dict(sorted(layer_lengths.items())),
        "track_widths": dict(sorted(widths.items())),
    }
    tables["route_lengths"] = dict(sorted(lengths.items(), key=lambda item: (-item[1], item[0])))

    copper_layers = board.GetCopperLayerCount()
    thickness_mm = mm(board.GetDesignSettings().GetBoardThickness())
    actual_copper_mm = first_number(
        source_text,
        r'\(layer\s+"F\.Cu"[\s\S]*?\(thickness\s+([0-9.]+)\)',
        0.035,
    )
    expected_copper_mm = float(profile.get("copper_thickness_um", actual_copper_mm * 1000.0)) / 1000.0
    stack_ok = (
        copper_layers == int(profile.get("copper_layers", copper_layers))
        and math.isclose(
            thickness_mm,
            float(profile.get("board_thickness_mm", thickness_mm)),
            abs_tol=0.01,
        )
        and math.isclose(actual_copper_mm, expected_copper_mm, abs_tol=0.001)
    )
    record(
        "stackup",
        "PASS" if stack_ok else "BLOCKING",
        f"{copper_layers} copper layers, {thickness_mm:.3f} mm board, "
        f"{actual_copper_mm * 1000.0:.1f} µm outer copper",
    )

    via_rule = profile.get("via_rule", {})
    via_failures = []
    for via in vias:
        diameter = mm(via.GetWidth(board.GetLayerID("F.Cu")))
        drill = mm(via.GetDrillValue())
        annular = (diameter - drill) / 2.0
        if via_rule and not (
            float(via_rule["drill_min_mm"]) <= drill <= float(via_rule["drill_max_mm"])
            and annular >= float(via_rule["annular_min_mm"])
        ):
            via_failures.append(f"{via.GetNetname()}@({mm(via.GetPosition().x):.2f},{mm(via.GetPosition().y):.2f}) {diameter:.2f}/{drill:.2f} mm")
    record("via geometry", "BLOCKING" if via_failures else "PASS", "; ".join(via_failures) if via_failures else f"All {len(vias)} vias meet the configured rule")
    reference_planes = dict(profile.get("reference_planes", {}))
    if not reference_planes:
        ground_zones = [zone for zone in board.Zones() if normalized_net(zone.GetNetname()) == "GND" and not zone.GetIsRuleArea()]
        routed_layers = sorted({segment.layer for segment in segments if normalized_net(segment.net) != "GND"})
        for signal_layer in routed_layers:
            candidate = next(
                (
                    (board.GetLayerName(layer), zone.GetNetname())
                    for zone in ground_zones
                    for layer in zone.GetLayerSet().Seq()
                    if board.GetLayerName(layer) != signal_layer
                ),
                None,
            )
            if candidate:
                reference_planes[signal_layer] = {"layer": candidate[0], "net": candidate[1]}
    plane_rows = []
    coverage_by_net: dict[str, dict[str, float]] = collections.defaultdict(lambda: {"covered": 0.0, "total": 0.0})
    for signal_layer, plane in reference_planes.items():
        plane_layer = str(plane["layer"])
        plane_net = normalized_net(str(plane["net"]))
        plane_layer_id = board.GetLayerID(plane_layer)
        zones = [zone for zone in board.Zones() if normalized_net(zone.GetNetname()) == plane_net and zone.GetLayerSet().Contains(plane_layer_id)]
        plane_area = sum(zone.GetFilledPolysList(plane_layer_id).Area() for zone in zones) / 1.0e12
        board_box = board.GetBoardEdgesBoundingBox()
        board_area = mm(board_box.GetWidth()) * mm(board_box.GetHeight())
        plane_rows.append((signal_layer, plane_layer, plane_net, plane_area, board_area, 100.0 * plane_area / board_area if board_area else 0.0))
        polygons = [zone.GetFilledPolysList(plane_layer_id) for zone in zones]
        for segment in [item for item in segments if item.layer == signal_layer and normalized_net(item.net) != plane_net]:
            sample_count = max(2, math.ceil(segment.length_mm / 0.25) + 1)
            covered = 0
            for index in range(sample_count):
                ratio = index / (sample_count - 1)
                x = segment.start[0] + ratio * (segment.end[0] - segment.start[0])
                y = segment.start[1] + ratio * (segment.end[1] - segment.start[1])
                point = pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
                covered += any(polygon.Contains(point) for polygon in polygons)
            coverage_by_net[segment.net]["total"] += segment.length_mm
            coverage_by_net[segment.net]["covered"] += segment.length_mm * covered / sample_count
    tables["planes"] = plane_rows
    tables["coverage"] = {
        net: (data["covered"], data["total"], 100.0 * data["covered"] / data["total"] if data["total"] else 0.0)
        for net, data in sorted(coverage_by_net.items())
    }
    poor_coverage = [(net, values[2]) for net, values in tables["coverage"].items() if values[1] >= 1.0 and values[2] < float(profile.get("minimum_reference_coverage_percent", 95.0))]
    if not reference_planes:
        record("return reference", "WARNING", "No reference plane could be configured or inferred")
    else:
        record("return reference", "WARNING" if poor_coverage else "PASS", "; ".join(f"{net} {coverage:.1f}%" for net, coverage in poor_coverage) if poor_coverage else "Configured or inferred signal layers have continuous reference under sampled routes")
    plane_nets = {str(item["layer"]): normalized_net(str(item["net"])) for item in reference_planes.values()}
    if plane_nets:
        non_plane_on_planes = sum(
            segment.length_mm
            for segment in segments
            if segment.layer in plane_nets
            and normalized_net(segment.net) != plane_nets[segment.layer]
        )
        record("plane cuts", "WARNING" if non_plane_on_planes > 0.0 else "PASS", f"{non_plane_on_planes:.2f} mm of non-reference-net routing lies on configured plane layers")

    epsilon_r = first_number(source_text, r"\(epsilon_r\s+([0-9.]+)\)", float(profile.get("epsilon_r", 4.3)))
    dielectric_mm = first_number(source_text, r'\(layer\s+"dielectric 1"[\s\S]*?\(thickness\s+([0-9.]+)\)', float(profile.get("dielectric_height_mm", thickness_mm - 0.07)))
    copper_mm = actual_copper_mm
    impedance_rows = []
    for width in sorted(widths):
        impedance, delay = microstrip(width, dielectric_mm, epsilon_r)
        hypothetical_mm = float(profile.get("hypothetical_plane_distance_mm", dielectric_mm))
        hypothetical_impedance, hypothetical_delay = microstrip(width, hypothetical_mm, epsilon_r)
        impedance_rows.append((width, impedance, delay, hypothetical_mm, hypothetical_impedance, hypothetical_delay))
    tables["impedance"] = impedance_rows
    hypothetical_mm = float(profile.get("hypothetical_plane_distance_mm", dielectric_mm))
    if impedance_rows and hypothetical_mm > 0.0:
        separation_ratio = dielectric_mm / hypothetical_mm
        tables["plane_comparison"] = {
            "current_mm": dielectric_mm,
            "hypothetical_mm": hypothetical_mm,
            "loop_area_ratio": separation_ratio,
            "idealized_db": 20.0 * math.log10(separation_ratio),
        }

    electrical_rows = []
    report_nets = profile.get("layout_report_nets")
    if report_nets is None:
        report_nets = sorted({segment.net for segment in segments if segment.layer in reference_planes})
    for net in report_nets:
        net_segments = [segment for segment in segments if segment.net == net and segment.layer in reference_planes]
        if not net_segments:
            continue
        coverage = tables["coverage"].get(net, (0.0, sum(item.length_mm for item in net_segments), 0.0))[2] / 100.0
        current_capacitance_pf = 0.0
        hypothetical_capacitance_pf = 0.0
        current_delay_ps = 0.0
        for segment in net_segments:
            impedance, delay = microstrip(segment.width_mm, dielectric_mm, epsilon_r)
            hypothetical_impedance, hypothetical_delay = microstrip(segment.width_mm, hypothetical_mm, epsilon_r)
            current_capacitance_pf += delay * segment.length_mm * coverage / impedance
            hypothetical_capacitance_pf += hypothetical_delay * segment.length_mm / hypothetical_impedance
            current_delay_ps += delay * segment.length_mm
        electrical_rows.append(
            (
                net,
                sum(item.length_mm for item in net_segments),
                coverage * 100.0,
                current_delay_ps,
                current_capacitance_pf,
                hypothetical_capacitance_pf,
                hypothetical_capacitance_pf / current_capacitance_pf if current_capacitance_pf else math.inf,
            )
        )
    tables["net_electrical"] = electrical_rows

    fast_rows = []
    for requested_net, rise_ns in profile.get("fast_edges_ns", {}).items():
        matching = next((row for row in impedance_rows if any(segment.net == requested_net and math.isclose(segment.width_mm, row[0]) for segment in segments)), None)
        if matching:
            critical_mm = float(rise_ns) * 1000.0 / (6.0 * matching[2])
            routed_mm = lengths.get(requested_net, 0.0)
            fast_rows.append((requested_net, float(rise_ns), routed_mm, critical_mm, routed_mm / critical_mm if critical_mm else 0.0))
    tables["fast_edges"] = fast_rows
    fast_warnings = [row for row in fast_rows if row[4] >= 1.0]
    record("transmission-line screen", "WARNING" if fast_warnings else "PASS", "; ".join(f"{row[0]} route/critical={row[4]:.2f}" for row in fast_warnings) if fast_warnings else "Configured on-board fast routes are shorter than one-sixth-rise-time screen; external cables are not included")

    adjacency_rows = []
    for sensitive in profile.get("sensitive_nets", []):
        for aggressor in profile.get("aggressor_nets", []):
            pairs = [(first, second) for first in segments for second in segments if first.net == sensitive and second.net == aggressor and first.layer == second.layer]
            if pairs:
                gap = min(segment_distance(first, second) for first, second in pairs)
                adjacency_rows.append((sensitive, aggressor, gap))
    tables["adjacency"] = adjacency_rows

    resistance_rows = []
    for net, current_ma in profile.get("supply_currents_ma", {}).items():
        resistance = sum(
            COPPER_RESISTIVITY_OHM_M * (segment.length_mm / 1000.0) / ((segment.width_mm / 1000.0) * (copper_mm / 1000.0))
            for segment in segments
            if segment.net == net
        )
        resistance_rows.append((net, float(current_ma), resistance, resistance * float(current_ma)))
    tables["supply_resistance"] = resistance_rows

    noise = profile.get("noise_model")
    if noise:
        gain = 1.0 + float(noise["feedback_ohm"]) / float(noise["gain_ohm"])
        bandwidth_hz = float(noise["gbw_hz"]) / gain
        noise_bandwidth_hz = math.pi / 2.0 * bandwidth_hz
        resistor_input_v = math.sqrt(4.0 * BOLTZMANN_J_K * float(noise.get("temperature_k", 300.0)) * float(noise["source_ohm"]) * noise_bandwidth_hz)
        amplifier_input_v = float(noise["voltage_noise_nv_sqrt_hz"]) * 1.0e-9 * math.sqrt(noise_bandwidth_hz)
        output_v = gain * math.hypot(resistor_input_v, amplifier_input_v)
        threshold_margin_v = float(noise.get("threshold_v", 0.0)) - float(noise.get("baseline_v", 0.0))
        tables["noise"] = {
            "gain": gain,
            "bandwidth_hz": bandwidth_hz,
            "noise_bandwidth_hz": noise_bandwidth_hz,
            "resistor_input_v": resistor_input_v,
            "amplifier_input_v": amplifier_input_v,
            "output_v": output_v,
            "threshold_margin_v": threshold_margin_v,
            "margin_sigma": threshold_margin_v / output_v if output_v > 0.0 else 0.0,
        }
        record("analytical noise floor", "WARNING", "Calculated a model-limited lower-bound; detector dark pulses, pickup, ripple, comparator noise, and stability peaking remain unmodeled")

    feedback = profile.get("feedback_net")
    if feedback and impedance_rows:
        feedback_length = lengths.get(str(feedback["net"]), 0.0)
        feedback_widths = [segment.width_mm for segment in segments if segment.net == feedback["net"]]
        if feedback_widths:
            width = collections.Counter(feedback_widths).most_common(1)[0][0]
            impedance, delay = microstrip(width, dielectric_mm, epsilon_r)
            capacitance_pf = delay * feedback_length / impedance
            pole_hz = 1.0 / (2.0 * math.pi * float(feedback["resistance_ohm"]) * capacitance_pf * 1.0e-12) if capacitance_pf else math.inf
            hypothetical_impedance, hypothetical_delay = microstrip(width, float(profile.get("hypothetical_plane_distance_mm", dielectric_mm)), epsilon_r)
            hypothetical_capacitance_pf = hypothetical_delay * feedback_length / hypothetical_impedance
            hypothetical_pole_hz = 1.0 / (2.0 * math.pi * float(feedback["resistance_ohm"]) * hypothetical_capacitance_pf * 1.0e-12) if hypothetical_capacitance_pf else math.inf
            tables["feedback"] = (feedback["net"], feedback_length, capacitance_pf, pole_hz, hypothetical_capacitance_pf, hypothetical_pole_hz)

    apply_expectations(
        board,
        source_text,
        profile.get("expect", {}),
        components,
        power_components,
        record,
        tables,
    )


def apply_expectations(
    board: Any,
    source_text: str,
    expected: dict[str, Any],
    components: list[dict[str, str]],
    power_components: list[dict[str, str]],
    record: Any,
    tables: dict[str, Any],
) -> None:
    if not expected:
        record("project expectations", "WARNING", "No project profile expectations were supplied")
        return
    box = board.GetBoardEdgesBoundingBox()
    origin = (mm(box.GetX()), mm(box.GetY()))
    actual_size = (mm(box.GetWidth()), mm(box.GetHeight()))
    y_up = expected.get("coordinate_system") == "lower_left_y_up"

    def design_position(position: Any) -> tuple[float, float]:
        x = mm(position.x) - origin[0]
        y = mm(position.y) - origin[1]
        return (x, actual_size[1] - y if y_up else y)

    wanted_size = tuple(float(value) for value in expected.get("outline_mm", actual_size))
    size_ok = all(math.isclose(actual, wanted, abs_tol=0.1) for actual, wanted in zip(actual_size, wanted_size))
    record("mechanical outline", "PASS" if size_ok else "BLOCKING", f"actual {actual_size[0]:.2f} x {actual_size[1]:.2f} mm; expected {wanted_size[0]:.2f} x {wanted_size[1]:.2f} mm")
    minimum_edge_arcs = int(expected.get("minimum_edge_arcs", 0))
    if minimum_edge_arcs:
        edge_arcs = source_text.count("(gr_arc")
        record(
            "mechanical outline",
            "PASS" if edge_arcs >= minimum_edge_arcs else "BLOCKING",
            f"Found {edge_arcs} outline arc primitives; require at least {minimum_edge_arcs}",
        )

    footprints = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}
    for reference, rule in expected.get("footprints", {}).items():
        footprint = footprints.get(reference)
        if footprint is None:
            record("footprint intent", "BLOCKING", f"Missing {reference}")
            continue
        failures = []
        if "side" in rule and footprint.GetLayerName() != rule["side"]:
            failures.append(f"side {footprint.GetLayerName()} != {rule['side']}")
        if "value_regex" in rule and not re.search(str(rule["value_regex"]), footprint.GetValue(), re.IGNORECASE):
            failures.append(f"value {footprint.GetValue()!r}")
        if "dnp" in rule and footprint.IsDNP() != bool(rule["dnp"]):
            failures.append(f"DNP={footprint.IsDNP()} != {bool(rule['dnp'])}")
        if "position_mm" in rule:
            position = design_position(footprint.GetPosition())
            wanted = tuple(float(value) for value in rule["position_mm"])
            if not all(math.isclose(actual, target, abs_tol=0.1) for actual, target in zip(position, wanted)):
                failures.append(f"position ({position[0]:.2f},{position[1]:.2f}) != ({wanted[0]:.2f},{wanted[1]:.2f})")
        if "rotation_deg" in rule:
            actual_rotation = footprint.GetOrientationDegrees() % 360.0
            wanted_rotation = float(rule["rotation_deg"]) % 360.0
            difference = abs((actual_rotation - wanted_rotation + 180.0) % 360.0 - 180.0)
            if difference > float(rule.get("rotation_tolerance_deg", 0.1)):
                failures.append(
                    f"rotation {actual_rotation:.1f} deg != {wanted_rotation:.1f} deg"
                )
        if "drill_mm" in rule:
            drills = [mm(pad.GetDrillSize().x) for pad in footprint.Pads() if mm(pad.GetDrillSize().x) > 0.0]
            if not drills or not all(math.isclose(value, float(rule["drill_mm"]), abs_tol=0.05) for value in drills):
                failures.append(f"drills {drills} != {rule['drill_mm']} mm")
        record("footprint intent", "BLOCKING" if failures else "PASS", f"{reference}: " + ("; ".join(failures) if failures else "matches configured side/value/geometry"))

    allowed_back = set(expected.get("allowed_back_footprints", []))
    unexpected_back = sorted(reference for reference, footprint in footprints.items() if footprint.GetLayerName() == "B.Cu" and reference not in allowed_back)
    missing_back = sorted(reference for reference in allowed_back if reference not in footprints or footprints[reference].GetLayerName() != "B.Cu")
    record("component sides", "BLOCKING" if unexpected_back or missing_back else "PASS", f"unexpected back={unexpected_back or 'none'}, required back missing={missing_back or 'none'}")

    for reference, pad_rules in expected.get("pad_nets", {}).items():
        footprint = footprints.get(reference)
        if footprint is None:
            continue
        pads = {pad.GetNumber(): normalized_net(pad.GetNetname()) for pad in footprint.Pads()}
        failures = []
        for number, wanted in pad_rules.items():
            actual = pads.get(number)
            if wanted is None:
                if actual is not None and not actual.startswith("unconnected-") and actual != "":
                    failures.append(f"pad {number}={actual}, expected NC")
            elif actual != normalized_net(str(wanted)):
                failures.append(f"pad {number}={actual or 'absent'}, expected {wanted}")
        record("critical pin mapping", "BLOCKING" if failures else "PASS", f"{reference}: " + ("; ".join(failures) if failures else "configured pad nets match"))
    for item in expected.get("absent_pads", []):
        reference, number = item.split(":", 1)
        footprint = footprints.get(reference)
        present = footprint is not None and any(pad.GetNumber() == number for pad in footprint.Pads())
        record("critical pin mapping", "BLOCKING" if present else "PASS", f"{reference} pad {number} is {'present' if present else 'absent as required'}")
    for item in expected.get("pad_quadrants", []):
        footprint = footprints.get(item["ref"])
        if footprint is None:
            continue
        pad = next((pad for pad in footprint.Pads() if pad.GetNumber() == str(item["pad"])), None)
        if pad is None:
            record("critical orientation", "BLOCKING", f"{item['ref']} pad {item['pad']} is absent")
            continue
        dx = mm(pad.GetPosition().x - footprint.GetPosition().x)
        dy = mm(pad.GetPosition().y - footprint.GetPosition().y)
        if y_up:
            dy = -dy
        actual = ("+" if dx > 0 else "-") + "X," + ("+" if dy > 0 else "-") + "Y"
        wanted = str(item["quadrant"])
        record("critical orientation", "PASS" if actual == wanted else "BLOCKING", f"{item['ref']} pad {item['pad']} is {actual}; expected {wanted}")

    proximity_rows = []
    for check in expected.get("proximity_checks", []):
        endpoints = []
        failures = []
        for endpoint in (check["first"], check["second"]):
            footprint = footprints.get(endpoint["ref"])
            pad = (
                next(
                    (
                        candidate
                        for candidate in footprint.Pads()
                        if candidate.GetNumber() == str(endpoint["pad"])
                    ),
                    None,
                )
                if footprint is not None
                else None
            )
            if pad is None:
                failures.append(f"missing {endpoint['ref']} pad {endpoint['pad']}")
            else:
                endpoints.append((mm(pad.GetPosition().x), mm(pad.GetPosition().y)))
        distance = math.dist(*endpoints) if len(endpoints) == 2 else math.inf
        maximum = float(check["max_mm"])
        if distance > maximum:
            failures.append(f"straight-line distance {distance:.2f} mm > {maximum:.2f} mm")
        status = "PASS" if not failures else str(check.get("failure_status", "BLOCKING"))
        record("placement proximity", status, f"{check['name']}: " + ("; ".join(failures) if failures else f"{distance:.2f} mm <= {maximum:.2f} mm"))
        proximity_rows.append((check["name"], distance, maximum, status))
    tables["proximity"] = proximity_rows

    component_values = [component["value"] for component in components]
    for rule in expected.get("component_counts", []):
        count = sum(bool(re.search(str(rule["value_regex"]), value, re.IGNORECASE)) for value in component_values)
        minimum = int(rule.get("min", 1))
        record("design implementation", "PASS" if count >= minimum else "BLOCKING", f"{rule['name']}: found {count}, require at least {minimum}")
    nets = {normalized_net(pad.GetNetname()) for footprint in board.GetFootprints() for pad in footprint.Pads()}
    for net in expected.get("required_nets", []):
        record("design implementation", "PASS" if normalized_net(net) in nets else "BLOCKING", f"Required net {net} {'exists' if normalized_net(net) in nets else 'is missing'}")
    test_points = sum(reference.startswith("TP") for reference in footprints)
    minimum_test_points = int(expected.get("minimum_test_points", 0))
    if minimum_test_points:
        record("test access", "PASS" if test_points >= minimum_test_points else "BLOCKING", f"Found {test_points} test-point footprints; require at least {minimum_test_points}")
    board_text = {
        drawing.GetText().strip()
        for drawing in board.GetDrawings()
        if hasattr(drawing, "GetText") and drawing.GetText().strip()
    }
    for required_text in expected.get("required_board_text", []):
        present = any(required_text.casefold() in text.casefold() for text in board_text)
        record("board markings", "PASS" if present else "BLOCKING", f"Required board text {required_text!r} {'exists' if present else 'is missing'}")
    if "related_component_regex" in expected:
        count = sum(bool(re.search(str(expected["related_component_regex"]), component["value"], re.IGNORECASE)) for component in power_components)
        record("related project", "PASS" if count else "BLOCKING", f"Related power/interface schematic has {count} component(s) matching {expected['related_component_regex']}")
    tables["components"] = components


def run_simulations(profile: dict[str, Any], root: Path, temporary: Path, record: Any, tables: dict[str, Any]) -> None:
    simulations = profile.get("simulations", [])
    if not simulations:
        record("circuit simulation", "WARNING", "No board-representative SPICE testbench is declared; simulation is NOT IMPLEMENTED")
        return
    ngspice = shutil.which("ngspice")
    if ngspice is None:
        record("circuit simulation", "BLOCKING", "ngspice is required by the declared simulations")
        return
    rows = []
    for simulation in simulations:
        netlist = (root / simulation["netlist"]).resolve()
        log = temporary / f"{simulation['name']}.log"
        completed = run([ngspice, "-b", "-o", str(log), str(netlist)], root)
        text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else completed.stdout + completed.stderr
        measurements = {}
        declared_measurements = {
            assertion["measurement"] for assertion in simulation.get("assertions", [])
        }
        for name, value in re.findall(r"(?mi)^\s*([a-z][a-z0-9_]*)\s*=\s*([-+0-9.e]+)", text):
            if declared_measurements and name not in declared_measurements:
                continue
            try:
                measurements[name] = float(value)
            except ValueError:
                pass
        failures = []
        for assertion in simulation.get("assertions", []):
            value = measurements.get(assertion["measurement"])
            if value is None or ("min" in assertion and value < float(assertion["min"])) or ("max" in assertion and value > float(assertion["max"])):
                failures.append(assertion["measurement"])
        status = "PASS" if completed.returncode == 0 and not failures else "BLOCKING"
        record("circuit simulation", status, f"{simulation['name']}: measurements={measurements or 'none'}, failed assertions={failures or 'none'}")
        rows.append((simulation["name"], status, measurements))
    tables["simulations"] = rows


def first_number(text: str, pattern: str, default: float) -> float:
    match = re.search(pattern, text)
    return float(match.group(1)) if match else default


def write_report(report_path: Path, base: Path, profile_path: Path | None, results: list[Result], tables: dict[str, Any]) -> None:
    overall = "DO NOT FABRICATE" if any(result.status == "BLOCKING" for result in results) else ("HUMAN REVIEW REQUIRED" if any(result.status == "WARNING" for result in results) else "READY FOR FINAL HUMAN REVIEW")
    lines = [
        f"# KiCad validation: {base.name}",
        "",
        f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}",
        f"Source: `{base}`",
        f"Profile: `{profile_path}`" if profile_path else "Profile: none (generic checks only)",
        f"Source PCB SHA-256: `{tables.get('source_hash', 'unavailable')}`",
        "",
        "## Overall status",
        "",
        f"**{overall}**",
    ]
    for status, heading in (("BLOCKING", "Blocking findings"), ("WARNING", "Warnings"), ("PASS", "Passed checks")):
        selected = [result for result in results if result.status == status]
        lines += ["", f"## {heading}", ""]
        lines += [f"- **{result.category}:** {result.message}" for result in selected] or ["- None."]

    inventory = tables.get("inventory")
    if inventory:
        lines += [
            "",
            "## Board and routing inventory",
            "",
            f"- {inventory['footprints']} footprints, {inventory['segments']} track segments, {inventory['vias']} vias, and {inventory['zones']} zones.",
            "- Track widths: " + (", ".join(f"{width:.3f} mm ({count} segments)" for width, count in inventory["track_widths"].items()) or "none") + ".",
            "- Routed copper by layer: " + (", ".join(f"{layer} {length:.2f} mm" for layer, length in inventory["tracks_by_layer_mm"].items()) or "none") + ".",
            "",
            "| Net | Routed length (mm) |",
            "|---|---:|",
        ]
        lines += [f"| `{net or '<no net>'}` | {length:.3f} |" for net, length in tables.get("route_lengths", {}).items()]

    if tables.get("planes"):
        lines += ["", "## Copper pour and return paths", "", "| Signal layer | Reference layer/net | Filled area (mm²) | Bounding-box coverage |", "|---|---|---:|---:|"]
        lines += [f"| {signal} | {plane} / `{net}` | {area:.1f} | {coverage:.1f}% |" for signal, plane, net, area, _board_area, coverage in tables["planes"]]
        lines += ["", "Sampled ground coverage directly below routed non-ground track centerlines:", "", "| Net | Covered / total (mm) | Coverage |", "|---|---:|---:|"]
        lines += [f"| `{net}` | {covered:.2f} / {total:.2f} | {percentage:.1f}% |" for net, (covered, total, percentage) in tables.get("coverage", {}).items()]

    if tables.get("impedance"):
        lines += [
            "",
            "## Layout-based signal calculations",
            "",
            "Zero-thickness microstrip approximation using the KiCad dielectric. The hypothetical column assumes a continuous closer ground plane at the stated distance; it is not a proposed stackup by itself.",
            "",
            "| Width | Current Z0 | Current delay | Hypothetical plane | Hypothetical Z0 | Hypothetical delay |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
        lines += [f"| {width:.3f} mm | {z0:.1f} Ω | {delay:.2f} ps/mm | {hyp_mm:.3f} mm | {hyp_z0:.1f} Ω | {hyp_delay:.2f} ps/mm |" for width, z0, delay, hyp_mm, hyp_z0, hyp_delay in tables["impedance"]]
    if tables.get("plane_comparison"):
        comparison = tables["plane_comparison"]
        lines += [
            "",
            f"Moving an uninterrupted signal return from {comparison['current_mm']:.3f} mm to {comparison['hypothetical_mm']:.3f} mm reduces the idealized signal/return loop area by {comparison['loop_area_ratio']:.2f}×. For equal current and geometry, magnetic-dipole radiation scales approximately with loop area, an idealized {comparison['idealized_db']:.1f} dB reduction. Slots, uncovered routes, connectors, and common-mode conversion can erase this benefit.",
        ]
    if tables.get("net_electrical"):
        lines += [
            "",
            "Per-net distributed effects on configured signal layers. Current capacitance counts only the sampled length with reference copper directly underneath; the hypothetical case assumes a continuous close plane.",
            "",
            "| Net | Routed length | Current coverage | Route delay sum | Current C | Close-plane C | C multiplier |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
        lines += [
            f"| `{net}` | {length:.2f} mm | {coverage:.1f}% | {delay:.1f} ps | {capacitance:.3f} pF | {hypothetical_capacitance:.3f} pF | {multiplier:.2f}× |"
            for net, length, coverage, delay, capacitance, hypothetical_capacitance, multiplier in tables["net_electrical"]
        ]
    if tables.get("fast_edges"):
        lines += ["", "| Fast net | Edge | Routed length | 1/6-edge critical length | Ratio |", "|---|---:|---:|---:|---:|"]
        lines += [f"| `{net}` | {edge:.2f} ns | {length:.2f} mm | {critical:.2f} mm | {ratio:.2f} |" for net, edge, length, critical, ratio in tables["fast_edges"]]
    if tables.get("feedback"):
        net, length, capacitance, pole, hypothetical_capacitance, hypothetical_pole = tables["feedback"]
        lines += [
            "",
            f"The `{net}` feedback route is {length:.2f} mm. Its distributed trace capacitance is approximately {capacitance:.2f} pF with the current reference distance and {hypothetical_capacitance:.2f} pF with the hypothetical close plane. If all of that capacitance appeared at the sensitive feedback node, its illustrative pole with the configured resistor would move from {pole / 1e6:.1f} MHz to {hypothetical_pole / 1e6:.1f} MHz. This bound is not a loop-stability simulation.",
        ]
    if tables.get("adjacency"):
        lines += ["", "Nearest same-layer copper-edge spacing for configured net pairs:", "", "| Sensitive net | Potential aggressor | Minimum gap |", "|---|---|---:|"]
        lines += [f"| `{sensitive}` | `{aggressor}` | {gap:.3f} mm |" for sensitive, aggressor, gap in tables["adjacency"]]
    if tables.get("proximity"):
        lines += ["", "Configured placement-proximity checks use pad-center straight-line distance; they are a lower bound on the routed supply/return loop.", "", "| Check | Distance | Limit | Status |", "|---|---:|---:|---|"]
        lines += [f"| {name} | {distance:.2f} mm | {maximum:.2f} mm | {status} |" for name, distance, maximum, status in tables["proximity"]]
    if tables.get("supply_resistance"):
        lines += ["", "35 µm copper bounds (all routed segments concatenated, so branched nets are conservatively overstated):", "", "| Net | Assumed current | Summed copper R | I×R bound |", "|---|---:|---:|---:|"]
        lines += [f"| `{net}` | {current:.2f} mA | {resistance * 1000:.2f} mΩ | {drop_mv:.3f} mV |" for net, current, resistance, drop_mv in tables["supply_resistance"]]
    if tables.get("noise"):
        noise = tables["noise"]
        lines += [
            "",
            "## Analytical noise floor",
            "",
            f"Configured noise gain is {noise['gain']:.2f}; estimated -3 dB bandwidth is {noise['bandwidth_hz'] / 1e6:.2f} MHz and one-pole noise bandwidth is {noise['noise_bandwidth_hz'] / 1e6:.2f} MHz. The selected source resistor contributes {noise['resistor_input_v'] * 1e6:.2f} µV RMS input-referred and the configured amplifier voltage-noise density contributes {noise['amplifier_input_v'] * 1e6:.2f} µV RMS input-referred. Their limited combined output estimate is {noise['output_v'] * 1e3:.3f} mV RMS; the configured threshold-to-baseline margin is {noise['threshold_margin_v'] * 1e3:.1f} mV ({noise['margin_sigma']:.0f} times this limited RMS model).",
            "",
            "This excludes detector dark pulses, comparator noise, bias/supply ripple, environmental pickup, resistor-network noise, parasitic peaking, and nonlinear recovery. It cannot predict the measured trigger rate.",
        ]
    if tables.get("simulations"):
        lines += [
            "",
            "## Circuit simulations",
            "",
            "These are deterministic, question-driven engineering models. Component and model limitations are stated in the corresponding netlists; a passing behavioral model does not replace bench qualification.",
            "",
            "| Simulation | Status | Measurements |",
            "|---|---|---|",
        ]
        for name, status, measurements in tables["simulations"]:
            rendered = ", ".join(
                f"`{key}`={value:.6g}" for key, value in sorted(measurements.items())
            ) or "none"
            lines.append(f"| {name} | {status} | {rendered} |")

    lines += [
        "",
        "## Interpretation limits",
        "",
        "- The checker refills zones and creates fabrication data from a temporary copy; it does not rewrite KiCad source.",
        "- Plane coverage is sampled along track centerlines. It reveals obvious return discontinuities but is not a 2D/3D field solve.",
        "- A closer ground plane generally tightens return current and reduces loop radiation, while lowering impedance and increasing trace/node capacitance. Sensitive high-impedance and feedback nodes must be re-laid out and simulated rather than covered indiscriminately.",
        "- External cable geometry, optical behavior, assembly orientation, component models, and physical measurements remain outside this automatic run.",
        "- Generated Gerbers/drills passing a smoke test is not manufacturing approval.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
